## **Objective**

**Flask-based web application** that collects, analyzes, and detects **scam advertisements** on social media using **web scraping, NLP, computer vision, and machine learning**. The system should have:

- A **structured backend** with Flask REST APIs.
- An **AI-powered scam detection engine** (NLP + Computer Vision).
- A **modern UI** using **Tailwind CSS** for an interactive dashboard.
- **Real-time alerts & scam reporting** features.

---

## **🛠️ Folder Structure & Functions**

```
php
CopyEdit
AdShield/
│── app/
│   ├── static/               # CSS, JS, Images
│   │   ├── styles.css        # Tailwind CSS
│   │   ├── scripts.js        # JS logic for interactivity
│   ├── templates/            # HTML templates (Jinja2)
│   │   ├── index.html        # Homepage UI
│   │   ├── dashboard.html    # Admin Dashboard
│   │   ├── reports.html      # Scam Reports
│   ├── routes/               # Flask route handlers
│   │   ├── api.py            # API endpoints for scam detection
│   │   ├── scraper.py        # Social media scraping logic
│   │   ├── ml_model.py       # AI-based scam detection logic
│   │   ├── alerts.py         # Real-time alert system
│   ├── __init__.py           # Flask app initialization
│── models/
│   ├── database.py           # Database schema (SQLite/MongoDB)
│── config.py                 # App configuration settings
│── main.py                   # Main Flask app entry point
│── requirements.txt           # Required Python libraries
│── README.md
                  # Documentation

```

---

## **🔹 Flask Routes & Functions**

### **1️⃣ `main.py` - Flask App Initialization**

- Initialize Flask app and register API routes.
- Run the server with debugging enabled.

---

### **2️⃣ `routes/api.py` - API for Scam Detection**

- `/api/detect_scam` (POST) → Analyze an ad using AI.
- `/api/get_reports` (GET) → Fetch scam reports from DB.
- `/api/alert_users` (POST) → Send alerts to users.

---

### **3️⃣ `routes/scraper.py` - Web Scraping for Ads**

- **Scrape targeted ads** from Facebook, Twitter, Instagram.
- Extract **text, images, videos, metadata**.
- Store ads in **MongoDB/SQLite database**.

---

### **4️⃣ `routes/ml_model.py` - AI-Based Scam Detection**

- **Text Processing:** NLP using `spaCy/BERT`.
- **Image Processing:** OCR using `Tesseract/OpenCV`.
- **ML Model:** Train and predict scam likelihood with `XGBoost`.

---

### **5️⃣ `routes/alerts.py` - Real-Time Alerts**

- Send **email, Telegram, or browser alerts** for scam detection.
- WebSockets for **real-time scam reporting**.

---

### **6️⃣ `models/database.py` - Database Schema**

- **Users Table** → Store user profiles & interactions.
- **Ads Table** → Store scraped ads & scam classifications.

---

# Configuration Guide

## Setting Up the Configuration

To use this project, you need to configure the environment variables properly. Follow the steps below to set up your `Config.py` file.

### 1. Create a Reddit App
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click on **Create an App** or **Create another App**
3. Fill in the necessary details:
   - **App name:** Choose a name for your app
   - **App type:** Select **script**
   - **Redirect URI:** Set it to `http://localhost`
   - **Permissions:** Grant necessary permissions
4. After creating the app, note down:
   - **Client ID** (Located under the app name)
   - **Client Secret** (Available in the app settings)

### 2. Configure Environment Variables
Set up the following environment variables:

```sh
export SECRET_KEY="your_secret_key"
export MONGO_URI="mongodb://localhost:27017/"
export DEBUG=True
export SOCKETIO_MESSAGE_QUEUE=None
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_reddit_username"
export REDDIT_PASSWORD="your_reddit_password"
export REDDIT_USER_AGENT="TrueADScraper/1.0"
```

Alternatively, you can add these variables to a `.env` file and load them using `dotenv`.

### 3. Configuration File (`Config.py`)
Create a `Config.py` file in your project directory with the following content:

```python
import os
import logging

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    logging.basicConfig(level=logging.ERROR)
    DEBUG = os.getenv("DEBUG", True)
    SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE", None)
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "abcdefghijkqwert")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "mnbvcxzasddfg")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "Hello-World")
    REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "Your Password")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TrueADScraper/1.0")
```

### 4. Run the Project
Once the configurations are set, run your project with:

```sh
python main.py
```

Ensure that your environment variables are loaded correctly to authenticate with Reddit and access the database properly.

---

This setup ensures secure and flexible configuration management for your project.



