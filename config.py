import os
import logging

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    logging.basicConfig(level=logging.ERROR)
    DEBUG = os.getenv("DEBUG", True)
    SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE", None)
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "WmtfK1cqa-krqHZJ9MEOtQ")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "Qr6SSk7x-XnI1xZVLou92ZTGVlmqsQ")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "Total-Log-3830")
    REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "mukesh@reddit")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TrueADScraper/1.0")