### 🚨 **TrueAD - AI-Powered Scam Advertisement Detection**

TrueAD is an AI-powered Flask-based web application that collects, analyzes, and detects scam advertisements on social media platforms in real-time using web scraping, NLP, computer vision, and machine learning.

<img src=logo.png alt=TrueAd-logo width="300"/>

### **🔧 Tech Stack**

- **Backend**: Flask (Python)
- **Web Scraping**: BeautifulSoup, Requests
- **NLP & ML**: spaCy, BERT, XGBoost
- **Image Processing**: Tesseract, OpenCV
- **Frontend**: Tailwind CSS, HTML, JavaScript
- **Database**: MongoDB or SQLite
- **Alerts**: Email, Telegram, WebSockets


### **⚙️ Features**

- **Real-time scam ad detection** from Facebook, Twitter, and Instagram.
- **Multi-layered scam detection** using ML, NLP, OCR, URL checks, and wallet blacklist verification.
- **Real-time alerts** sent via email, Telegram, or browser notifications.
- **Admin Dashboard** to manage ads and view flagged reports.
- **AI-powered text and image processing** for enhanced scam detection.
- **Modular architecture** for easy scalability and maintenance.


### **🛠️ Setup Instructions**

### 1. 📦 **Prerequisites**

Ensure you have the following installed:

- Python 3.8+
- MongoDB (or SQLite for local setup)
- pip (Python package manager)


### 2. 🔑 **Configuration**

Create or update the `config.py` file with the following structure:

```python

class Config:
    SECRET_KEY = "your_secret_key"
    MONGO_URI = "mongodb://localhost:27017/"
    DEBUG = True
    REDDIT_CLIENT_ID = "your_client_id"
    REDDIT_CLIENT_SECRET = "your_client_secret"
    REDDIT_USERNAME = "your_reddit_username"
    REDDIT_PASSWORD = "your_reddit_password"
    REDDIT_USER_AGENT = "TrueADScraper/1.0"

```


### 3. 📥 **Install Dependencies**

Install the required dependencies:

```bash
pip install -r requirements.txt

```

If `requirements.txt` is missing, install manually:

```bash
pip install flask beautifulsoup4 requests spacy xgboost opencv-python

```


### **🚀 Running the App**

Use two terminal tabs:

- **Terminal 1**: Start Flask Backend
    
```bash
python main.py
    
```
    
- **Terminal 2**: Start Social Media Scraping and AI Monitoring
    
```bash
python scraper.py
    
```
    

Open your browser and visit: `http://localhost:5000`


### **📊 Risk Scoring Breakdown**

| Detection Technique | Weight Added |
| --- | --- |
| ML Model Prediction | +0.6 |
| Keyword Match | +0.5 |
| Phishing URL Detected | +0.6 |
| Crypto Wallet Blacklist Match | +0.7 |
| NLP Embedding Match (Semantic) | +0.2 |
| OCR-based Scam Text Detection | +0.3 |

**Messages are flagged if the total risk score > 0.4** (default threshold).


### **🙌 Contribution Guidelines**

### 🔧 **Want to Contribute?**

We welcome contributions from developers!

📌 **Here's how you can help**:

- Improve scam detection accuracy (enhance ML models or NLP logic).
- Add support for more scam patterns or keywords.
- Refactor code for modularity and scalability.
- UI/UX improvements for the dashboard.
- Write documentation or create test cases.


### 🛠️ **To Contribute:**

1. Fork this repository.
2. Create a new branch (feature/your-feature-name).
3. Commit your changes with clear messages.
4. Push to your branch and create a Pull Request.


### **🧠 Future Enhancements**

- Admin login & access control.
- Visual scam heatmaps & statistics.
- PDF export of scam reports.
- Multilingual support.
- Integration with Discord, WhatsApp, etc.


### **📬 Contact**

For support, questions, or collaboration:

- 📧 Email: [mukeshkumar.cse24@gmail.com]


### **📄 License**

This project is licensed under the MIT License.