# routes/api.py - Enhanced API Endpoints for Scam Detection with Debugging and Classified Ads Display
import logging
from flask import Blueprint, request, jsonify
from models.database import init_db
from app.routes.ml_model import predict_scam
from app.extensions import socketio 
import uuid  # ✅ Import UUID for unique ad IDs
from pymongo import MongoClient
from config import Config

# Initialize database connection
db = init_db()
api_blueprint = Blueprint("api", __name__)

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Detect Scam API - Debugging Added
@api_blueprint.route("/detect_scam", methods=["POST"])
def detect_scam():
    print("✅ API /detect_scam was called!")

    data = request.json
    print(f"📩 Received request data: {data}")

    if not data or "text" not in data:
        print("❌ Invalid request format or missing 'text' key.")
        return jsonify({"error": "Invalid request format. 'text' field is required."}), 400

    ad_text = data["text"].strip()  # Ensure text is properly stripped
    if not ad_text:
        print("⚠️ No ad text provided.")
        return jsonify({"error": "Ad text is required"}), 400

    # ✅ Call the ML Model with correct argument
    prediction = predict_scam(ad_text)

    if not isinstance(prediction, dict) or "is_scam" not in prediction or "confidence" not in prediction:
        print("❌ Error: predict_scam() returned an invalid response:", prediction)
        return jsonify({"error": "Prediction failed"}), 500

    scam_status = bool(prediction.get("is_scam"))  # Ensure it's a boolean
    confidence = float(prediction.get("confidence"))  # Ensure it's a float
    ad_id = str(uuid.uuid4())  # ✅ Generate unique ID for tracking

    try:
        result = db["ads"].insert_one({
            "ad_id": ad_id,
            "text": ad_text,
            "is_scam": scam_status,
            "confidence": confidence
        })
        print(f"✅ Scam report saved in MongoDB! ID: {result.inserted_id}")
    except Exception as e:
        print(f"❌ Database Insert Error: {e}")
        return jsonify({"error": "Database insert failed"}), 500

    # ✅ Return a clean response
    return jsonify({
        "ad_id": ad_id,
        "is_scam": scam_status,
        "confidence": confidence
    })

# Get Scam Reports - Adding Pagination & Search
@api_blueprint.route("/get_reports", methods=["GET"])
def get_reports():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    search_query = request.args.get("search", "")
    
    logger.debug(f"Fetching reports - Page: {page}, Per Page: {per_page}, Search Query: {search_query}")
    
    query = {}
    if search_query:
        query["text"] = {"$regex": search_query, "$options": "i"}  # Case-insensitive search
    
    total_reports = db["ads"].count_documents(query)
    reports = list(db["ads"].find(query, {"_id": 0}))
    
    return jsonify({
        "reports": reports,
        "total": total_reports,
        "page": page,
        "per_page": per_page
    })

# Fetch Classified Ads - Display Ads from Reddit or Other Sources
@api_blueprint.route("/get_classified_ads", methods=["GET"])
def get_classified_ads():
    try:
        ads = list(db["classified_ads"].find({}, {"_id": 0}))
        return jsonify({"ads": ads, "total": len(ads)})
    except Exception as e:
        logger.error(f"Error fetching classified ads: {e}")
        return jsonify({"error": "Failed to fetch classified ads"}), 500

# Alert Users - Send Real-Time Alerts via WebSockets
@api_blueprint.route("/alert_users", methods=["POST"])
def alert_users():
    data = request.json
    logger.debug(f"Alert data received: {data}")
    
    message = data.get("message", "Scam alert detected!")
    socketio.emit("scam_alert", {"message": message})
    return jsonify({"status": "Alert sent", "message": message})

db_client = MongoClient(Config.MONGO_URI)
db = db_client["TrueAD"]

@api_blueprint.route("/process_reddit_ads", methods=["POST"])
def process_reddit_ads():
    reddit_ads = db["reddit_ads"].find()  # Get fetched Reddit ads
    processed_ads = []

    for ad in reddit_ads:
        scam_result = predict_scam(ad["text"])  # Run scam detection
        ad.update(scam_result)  # Add classification result to ad
        db["ads"].update_one({"ad_id": ad["ad_id"]}, {"$set": ad}, upsert=True)  # Store in ads collection
        processed_ads.append(ad)

    return jsonify({"message": "Reddit ads processed successfully", "processed_ads": processed_ads})