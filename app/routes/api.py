# routes/api.py - Enhanced API Endpoints for Scam Detection with Debugging and Classified Ads Display
import logging
import uuid
import requests
import easyocr
from flask import Blueprint, request, jsonify
from models.database import init_db
from app.routes.ml_model import predict_scam
from app.extensions import socketio 
from pymongo import MongoClient
from config import Config

# Initialize database connection
db = init_db()
api_blueprint = Blueprint("api", __name__)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_url_safety(url):
    api_key = Config.GOOGLE_SAFE_BROWSING_API_KEY
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {"clientId": "TrueAD", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    response = requests.post(api_url, json=payload)
    result = response.json()
    return bool(result.get("matches"))

def process_image_text(image):
    reader = easyocr.Reader(["en"])
    extracted_text = reader.readtext(image, detail=0)
    text_combined = " ".join(extracted_text)
    return predict_scam(text_combined)

@api_blueprint.route("/submit_report", methods=["POST"])
def submit_report():
    data = request.form
    ad_url = data.get("ad_url", "").strip()
    description = data.get("description", "").strip()
    proof_images = request.files.getlist("proof_images")

    if not ad_url and not description:
        return jsonify({"error": "Ad URL or description is required"}), 400
    
    url_scam = check_url_safety(ad_url) if ad_url else False
    scam_prediction = predict_scam(description) if description else {"is_scam": False, "confidence": 0}

    report_data = {
        "report_id": str(uuid.uuid4()),
        "ad_url": ad_url,
        "description": description,
        "is_scam": url_scam or scam_prediction["is_scam"],
        "confidence": max(scam_prediction["confidence"], 1.0 if url_scam else 0.0),
        "status": "Pending"
    }
    db["reports"].insert_one(report_data)
    return jsonify({"message": "Report submitted successfully", "report": report_data})

@api_blueprint.route("/get_reported_ads", methods=["GET"])
def get_reported_ads():
    reports = list(db["reports"].find({}, {"_id": 0}))
    return jsonify({"reports": reports})

@api_blueprint.route("/approve_report", methods=["POST"])
def approve_report():
    report_id = request.json.get("report_id")
    db["reports"].update_one({"report_id": report_id}, {"$set": {"status": "Approved"}})
    return jsonify({"message": "Report approved"})

@api_blueprint.route("/reject_report", methods=["POST"])
def reject_report():
    report_id = request.json.get("report_id")
    db["reports"].update_one({"report_id": report_id}, {"$set": {"status": "Rejected"}})
    return jsonify({"message": "Report rejected"})

@api_blueprint.route("/detect_scam", methods=["POST"])
def detect_scam():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request format. 'text' field is required."}), 400
    
    ad_text = data["text"].strip()
    prediction = predict_scam(ad_text)
    scam_status = bool(prediction.get("is_scam"))
    confidence = float(prediction.get("confidence"))
    ad_id = str(uuid.uuid4())

    db["ads"].insert_one({"ad_id": ad_id, "text": ad_text, "is_scam": scam_status, "confidence": confidence})
    return jsonify({"ad_id": ad_id, "is_scam": scam_status, "confidence": confidence})

@api_blueprint.route("/get_reports", methods=["GET"])
def get_reports():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    query = {}
    total_reports = db["ads"].count_documents(query)
    reports = list(db["ads"].find(query, {"_id": 0}))
    return jsonify({"reports": reports, "total": total_reports, "page": page, "per_page": per_page})

@api_blueprint.route("/process_reddit_ads", methods=["POST"])
def process_reddit_ads():
    reddit_ads = db["reddit_ads"].find()
    processed_ads = []
    for ad in reddit_ads:
        scam_result = predict_scam(ad["text"])
        ad.update(scam_result)
        db["ads"].update_one({"ad_id": ad["ad_id"]}, {"$set": ad}, upsert=True)
        processed_ads.append(ad)
    return jsonify({"message": "Reddit ads processed successfully", "processed_ads": processed_ads})
