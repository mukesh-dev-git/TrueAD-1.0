# routes/scraper.py - Web Scraper for Social Media Ads
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify
from models.database import init_db

scraper_blueprint = Blueprint("scraper", __name__)

db = init_db()

@scraper_blueprint.route("/scrape_ads", methods=["POST"])
def scrape_ads():
    data = request.json
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch the page"}), 500
    
    soup = BeautifulSoup(response.text, "html.parser")
    ad_texts = [p.text for p in soup.find_all("p")]
    ad_images = [img["src"] for img in soup.find_all("img") if "src" in img.attrs]
    
    scraped_data = {
        "url": url,
        "text": " ".join(ad_texts),
        "images": ad_images
    }
    
    db["ads"].insert_one(scraped_data)
    
    return jsonify({"message": "Ad scraped successfully", "data": scraped_data})
