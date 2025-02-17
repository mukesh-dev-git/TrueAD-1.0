import joblib
import xgboost as xgb
import numpy as np
import requests
import easyocr
from flask import Blueprint, request, jsonify
from config import Config
from sklearn.feature_extraction.text import TfidfVectorizer

ml_model_blueprint = Blueprint("ml_model", __name__)

# Load the trained model and vectorizer
model = joblib.load("models/xgboost_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
reader = easyocr.Reader(["en"])  # OCR model

def check_url_safety(url):
    """
    Check if a given URL is safe using Google's Safe Browsing API.
    """
    api_key = Config.GOOGLE_SAFE_BROWSING_API_KEY
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {
            "clientId": "truead", "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    response = requests.post(endpoint, json=payload)
    data = response.json()
    return bool(data.get("matches"))

def extract_text_from_image(image_path):
    """ Extract text from an image using EasyOCR. """
    return " ".join(reader.readtext(image_path, detail=0))

def predict_scam(text, url=None, image_path=None):
    """
    Predict whether a given input (text, URL, image) is a scam.
    """
    is_scam = False
    confidence = 0.0
    
    if url:
        if check_url_safety(url):
            is_scam = True
            confidence = 1.0
    
    if image_path:
        extracted_text = extract_text_from_image(image_path)
        text += " " + extracted_text
    
    transformed_text = vectorizer.transform([text])
    prediction = model.predict(transformed_text)[0]
    confidence = max(confidence, np.max(model.predict_proba(transformed_text)))
    is_scam = is_scam or bool(prediction)
    
    return {"is_scam": is_scam, "confidence": float(confidence)}

@ml_model_blueprint.route("/predict_scam", methods=["POST"])
def predict_scam_api():
    try:
        data = request.json
        text = data.get("text", "")
        url = data.get("url", None)
        image_path = data.get("image_path", None)
        result = predict_scam(text, url, image_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
