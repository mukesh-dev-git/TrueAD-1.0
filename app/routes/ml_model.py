import joblib
import xgboost as xgb
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Blueprint, request, jsonify

ml_model_blueprint = Blueprint("ml_model", __name__)

# Load the trained model and vectorizer
model = joblib.load("models/xgboost_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

def predict_scam(text):
    """
    Predict whether a given text is a scam (spam) or not.
    :param text: Input advertisement text
    :return: Dictionary with 'is_scam' boolean and 'confidence' score
    """
    transformed_text = vectorizer.transform([text])
    prediction = model.predict(transformed_text)[0]
    confidence = np.max(model.predict_proba(transformed_text))
    
    return {"is_scam": bool(prediction), "confidence": float(confidence)}

@ml_model_blueprint.route("/predict_scam", methods=["POST"])
def predict_scam_api():
    try:
        ad_text = request.json.get("text", "")
        result = predict_scam(ad_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})
