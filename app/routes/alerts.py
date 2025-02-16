# routes/alerts.py - Real-Time Alerts using WebSockets
from flask import Blueprint, request, jsonify
from flask_socketio import emit
from main import socketio

alerts_blueprint = Blueprint("alerts", __name__)

@alerts_blueprint.route("/send_alert", methods=["POST"])
def send_alert():
    data = request.json
    message = data.get("message", "Scam alert detected!")
    
    # Emit WebSocket event
    socketio.emit("scam_alert", {"message": message})
    
    return jsonify({"status": "Alert sent", "message": message})
