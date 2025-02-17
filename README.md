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


