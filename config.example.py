import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE", None)

    GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY", "")

    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "")
    REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TrueADScraper/1.0")
