<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,100:2563EB&height=200&section=header&text=TrueAD&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Scam%20Advertisement%20Detection%20Prototype&descAlignY=58&descSize=18" width="100%" alt="TrueAD banner"/>

<a href="#-detection-pipeline"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1200&color=2563EB&center=true&vCenter=true&width=720&lines=Scam+advertisement+detection+with+Flask+%2B+XGBoost;Reddit+ingestion+%C2%B7+TF-IDF+%C2%B7+EasyOCR+%C2%B7+Safe+Browsing;Report+portal+and+dashboard+backed+by+MongoDB;Prototype+built+Feb%E2%80%93Apr+2025" alt="Typing summary"/></a>

<br/>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-010101?logo=socketdotio&logoColor=white)](https://flask-socketio.readthedocs.io)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-337AB7)](https://xgboost.readthedocs.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Reddit](https://img.shields.io/badge/Reddit-PRAW-FF4500?logo=reddit&logoColor=white)](https://praw.readthedocs.io)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CDN-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org)
<br/>
[![Status](https://img.shields.io/badge/Status-Prototype%20%C2%B7%20Archived-F97316)](#-status-and-known-limitations)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

</div>

---

## <img src="https://api.iconify.design/lucide/target.svg?color=%232563EB" width="26" align="top" alt=""/> Project Overview

TrueAD classifies advertisement text as **scam or safe**. It has a Flask backend with a JSON API, a MongoDB store, a **TF-IDF + XGBoost** text classifier trained on a spam/ham dataset, an optional **Google Safe Browsing** URL check, optional **EasyOCR** text extraction from images, and a small dashboard with charts and a report portal. A separate script pulls candidate ads from a subreddit through the Reddit API so they can be scored in bulk.

It was built in February 2025 and last updated in April 2025. The text-classification path and the dashboard work; several things in the original plan were never connected, listed in [Status and known limitations](#-status-and-known-limitations).

### Key Features

- <img src="https://api.iconify.design/lucide/brain-circuit.svg?color=%237C3AED" width="18" align="top" alt=""/> **Text classifier**: TF-IDF (5,000 features) into an XGBoost model, trained by `train_xgboost.py` on `spam_vs_ham.csv` (80/20 split).
- <img src="https://api.iconify.design/lucide/link.svg?color=%230EA5E9" width="18" align="top" alt=""/> **URL check**: submitted ad URLs are checked against the Google Safe Browsing API and force a scam verdict on a match.
- <img src="https://api.iconify.design/lucide/flag.svg?color=%23F59E0B" width="18" align="top" alt=""/> **Report portal**: users submit an ad URL and description; each report gets a verdict and a confidence value.
- <img src="https://api.iconify.design/lucide/layout-dashboard.svg?color=%2310B981" width="18" align="top" alt=""/> **Dashboard**: overall statistics, paginated and searchable reports, and settings pages.
- <img src="https://api.iconify.design/lucide/download-cloud.svg?color=%23EF4444" width="18" align="top" alt=""/> **Reddit ingestion**: `reddit_scraper.py` stores recent subreddit posts, and `/api/process_reddit_ads` scores them.

## <img src="https://api.iconify.design/lucide/image.svg?color=%232563EB" width="26" align="top" alt=""/> Screenshots

| Dashboard | Reports | Overview |
|---|---|---|
| <img src="Screenshots_video/Dashboard%201.png" alt="Dashboard"/> | <img src="Screenshots_video/Reports%201.png" alt="Reports"/> | <img src="Screenshots_video/Overview.png" alt="Overview"/> |

More captures and a demo video are in [`Screenshots_video/`](Screenshots_video/).

## <img src="https://api.iconify.design/lucide/network.svg?color=%232563EB" width="26" align="top" alt=""/> Detection Pipeline

```mermaid
flowchart TD
    R[Reddit subreddit<br/>reddit_scraper.py + PRAW] --> RA[(MongoDB<br/>reddit_ads)]
    U[User report form<br/>ad URL + description] --> API[Flask API<br/>app/routes/api.py]
    RA -->|POST /api/process_reddit_ads| P
    API --> P{predict_scam<br/>ml_model.py}
    API -->|ad URL| S[Google Safe Browsing<br/>URL check]
    P --> T[TF-IDF + XGBoost<br/>text verdict + confidence]
    S --> V[Final verdict<br/>scam if URL match or model says scam]
    T --> V
    V --> D[(MongoDB<br/>ads, reports)]
    D --> UI[Dashboard + reports pages]

    classDef src fill:#F1EFE8,stroke:#888780,color:#222
    classDef det fill:#EEEDFE,stroke:#7F77DD,color:#222
    classDef out fill:#2563EB,stroke:#0F172A,color:#fff
    class R,RA,U src
    class API,P,S,T,V det
    class D,UI out
```

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%232563EB" width="26" align="top" alt=""/> Requirements

- Python 3.8+
- MongoDB running locally (or a connection string in `MONGO_URI`)
- Optional: a Google Safe Browsing API key, and a Reddit script app for the scraper
- Internet access on first run to download the EasyOCR models, and for the Tailwind and Chart.js CDNs used by the pages

## <img src="https://api.iconify.design/lucide/zap.svg?color=%232563EB" width="26" align="top" alt=""/> Quick Start

### Installation

```bash
git clone https://github.com/mukesh-dev-git/TrueAD-1.0.git
cd TrueAD-1.0

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

`config.py` is gitignored. Copy the template and fill in what you need:

```bash
cp config.example.py config.py
```

| Setting | Used by | Required |
|---|---|---|
| `SECRET_KEY` | Flask | Yes (change it) |
| `MONGO_URI` | database and scraper | Yes (defaults to local MongoDB) |
| `GOOGLE_SAFE_BROWSING_API_KEY` | URL check in `/api/submit_report` | Only for URL reports |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, `REDDIT_USER_AGENT` | `reddit_scraper.py` | Only for the scraper |

Set them as environment variables, or edit `config.py` locally. Never commit real keys or passwords.

### Run

```bash
python main.py                 # dashboard and API at http://localhost:5000
python reddit_scraper.py       # optional: pull recent posts from a subreddit into MongoDB
```

### Retrain the model (optional)

The trained model and vectorizer are committed in `models/`. To rebuild them:

```bash
python train_xgboost.py        # reads spam_vs_ham.csv, writes models/xgboost_model.pkl and tfidf_vectorizer.pkl
```

## <img src="https://api.iconify.design/lucide/plug.svg?color=%232563EB" width="26" align="top" alt=""/> API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/detect_scam` | JSON `{"text": "..."}` returns verdict and confidence, and stores the ad |
| POST | `/api/submit_report` | Form with `ad_url`, `description`, optional `proof_images` creates a report |
| GET | `/api/get_reported_ads` | Paginated reports, with `page`, `per_page` and `search` |
| GET | `/api/get_reports` | Paginated scored ads |
| GET | `/api/get_overall_statistics` | Scam/safe counts and average confidence |
| POST | `/api/process_reddit_ads` | Score everything in `reddit_ads` |

Pages: `/` and `/dashboard`, `/reports`, `/settings`.

## <img src="https://api.iconify.design/lucide/folder-tree.svg?color=%232563EB" width="26" align="top" alt=""/> Project Structure

```
TrueAD-1.0/
├── main.py                  # Flask + Socket.IO app, page routes
├── config.example.py        # settings template (copy to config.py)
├── app/
│   ├── extensions.py        # Socket.IO instance
│   ├── routes/              # api.py (registered), ml_model.py, alerts.py, scraper.py
│   ├── templates/           # dashboard, reports, settings, layout
│   └── static/              # scripts.js, styles.css
├── models/                  # database.py, xgboost_model.pkl, tfidf_vectorizer.pkl
├── reddit_scraper.py        # Reddit ingestion script
├── train_xgboost.py         # model training
├── del_scam.py              # clears the ads collection
├── spam_vs_ham.csv          # training data
└── Screenshots_video/
```

## <img src="https://api.iconify.design/lucide/gauge.svg?color=%232563EB" width="26" align="top" alt=""/> Status and Known Limitations

This is a prototype. What is and is not in place:

| Area | State |
|---|---|
| Text classification (`/api/detect_scam`) | Working |
| Report submission with URL check | Working when a Safe Browsing key is set |
| Dashboard, reports and statistics pages | Working |
| Reddit ingestion and bulk scoring | Working when Reddit credentials are set |
| Image proof upload | Files are accepted but not processed; the OCR helper is never called from the report route |
| Real-time alerts (Socket.IO) | The server is initialised, but the alert route is written and never registered, so no alerts are sent |
| `ml_model.py` and `scraper.py` routes | Written but not registered in `main.py` |
| User accounts | A `users` collection and index exist; there is no login |
| Facebook, Twitter and Instagram scraping | Not implemented (only Reddit) |
| Confidence value | The highest class probability, so for a "safe" verdict it is confidence in "safe", not a scam probability |
| Tests and deployment | Not implemented |

### External services

| Service | Used for | Needed to run? |
|---|---|---|
| MongoDB (local) | Ads, reports, Reddit posts | Yes |
| Google Safe Browsing API | URL checks | Only for URL reports |
| Reddit API (script app) | Scraper | Only for the scraper |
| EasyOCR model download | OCR helper | Yes, on first import |
| Tailwind and Chart.js CDNs | Frontend styling and charts | Yes, for the pages to render |

## <img src="https://api.iconify.design/lucide/lightbulb.svg?color=%232563EB" width="26" align="top" alt=""/> Ideas for Next Steps

- Register the alerts, scraper and ML blueprints, and call the OCR helper for uploaded proof images
- Return a real scam probability instead of the top class probability
- Add authentication and persist the settings page
- Add tests and a reproducible environment

## <img src="https://api.iconify.design/lucide/scale.svg?color=%232563EB" width="26" align="top" alt=""/> License

MIT. See [LICENSE](LICENSE).

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2563EB,100:0F172A&height=110&section=footer&animation=fadeIn" width="100%" alt=""/>

</div>
