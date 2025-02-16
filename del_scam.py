from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["TrueAD"]  # Replace with your actual DB name

# Clear all stored scam reports
db["ads"].delete_many({})
print("✅ All scam reports cleared!")
