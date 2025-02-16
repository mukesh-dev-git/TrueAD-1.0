from flask import Flask
from flask_cors import CORS
from config import Config
from app.routes.api import api_blueprint
from models.database import init_db
from app.extensions import socketio  # Import from new file

# Initialize Flask app
app = Flask(__name__, template_folder="app/templates")
app.config.from_object(Config)
CORS(app)  
socketio.init_app(app)  # Initialize socketio with Flask app

# Register Blueprints
app.register_blueprint(api_blueprint, url_prefix="/api")

# Initialize Database
init_db()

from flask import render_template

@app.route("/")
def home():
    return render_template("dashboard.html") 

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
