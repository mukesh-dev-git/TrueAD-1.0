from pymongo import MongoClient
from config import Config

def init_db():
    client = MongoClient(Config.MONGO_URI)
    db = client["TrueAD"]  # Ensure database selection

    # Define collections
    users = db["users"]
    ads = db["ads"]
    reports = db["reports"]

    # Indexing for faster lookups
    users.create_index("email", unique=True)
    ads.create_index("ad_id", unique=True)
    reports.create_index("report_id", unique=True)

    print("[INFO] Database initialized successfully.")
    return db  # Return the database instance
