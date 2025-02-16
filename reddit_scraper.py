import praw
import os
import json
from pymongo import MongoClient
from config import Config

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    username=Config.REDDIT_USERNAME,
    password=Config.REDDIT_PASSWORD,
    user_agent=Config.REDDIT_USER_AGENT
)

# Connect to MongoDB
db_client = MongoClient(Config.MONGO_URI)
db = db_client["TrueAD"]
ads_collection = db["reddit_ads"]

# Function to fetch ads from Reddit
def fetch_reddit_ads(subreddit="advertising", limit=50):
    print(f"🔍 Fetching ads from r/{subreddit}...")
    try:
        subreddit_obj = reddit.subreddit(subreddit)
        posts = subreddit_obj.new(limit=limit)
        
        ads = []
        for post in posts:
            if not post.stickied:  # Ignore stickied posts
                ad_data = {
                    "ad_id": post.id,
                    "title": post.title,
                    "text": post.selftext,
                    "url": post.url,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "created_utc": post.created_utc
                }
                ads.append(ad_data)
                
                # Store in MongoDB if not already present
                if not ads_collection.find_one({"ad_id": post.id}):
                    ads_collection.insert_one(ad_data)
        
        print(f"✅ Fetched {len(ads)} ads from r/{subreddit}.")
        return ads
    except Exception as e:
        print(f"❌ Error fetching Reddit ads: {e}")
        return []

if __name__ == "__main__":
    fetch_reddit_ads()
