<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=🛡️+NetGuard+MLOps;Phishing+URL+Detection;Real-Time+%7C+ML-Powered+%7C+Cloud-Native" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20ECR%20%7C%20S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![DagsHub](https://img.shields.io/badge/DagsHub-Experiment%20Tracking-FF6B35?style=for-the-badge)](https://dagshub.com)

<br/>

> **Production-grade MLOps pipeline** — type in a raw URL and get an instant phishing verdict with live feature extraction, ensemble ML, and CI/CD to AWS.

<br/>

[🚀 Quick Start](#-quick-start) · [🏗️ Architecture](#%EF%B8%8F-architecture) · [🌐 API Reference](#-api-reference) · [🤖 ML Models](#-ml-models) · [☁️ Deployment](#%EF%B8%8F-deployment)

</div>

---

## 🆕 What's New in This Version

| Feature | Previous | This Version |
|---|---|---|
| **Live URL Scan** | ❌ Not supported | ✅ Type any raw URL → instant verdict |
| **Feature Extraction** | Manual / static CSVs | Live 24/30 features extracted in real-time |
| **API Endpoints** | 2 (`/train`, `/predict`) | 4 (`/train`, `/predict`, `/predict_url`, `/predict_url_csv`) |
| **Frontend** | Bare Swagger UI | Full custom HTML dashboard |
| **Batch URL Mode** | Pre-built feature CSVs only | Raw URL CSVs — auto-extract & classify |
| **Dependency** | `requests` minimal | + `beautifulsoup4` for real HTML scraping |

---

## ✨ What It Does

```
You type:   https://totally-not-phishing.free.win.xyz/login/paypal
Model says: 🔴 MALICIOUS  (24 features computed live in ~1.2s)
```

**NetGuard** is an end-to-end machine learning system that detects phishing URLs using 30 URL and network-behavioural features. Feed it a raw URL, a CSV of features, or a CSV of raw URLs — it classifies all of them.

---

## 🏗️ Architecture

```
                        ┌─────────────────────────────────────────┐
                        │            USER INTERFACES               │
                        │  Browser UI  │  REST API  │  CSV Upload  │
                        └──────────────────┬──────────────────────┘
                                           │
                        ┌──────────────────▼──────────────────────┐
                        │           FastAPI Application            │
                        │  /predict_url   /predict   /predict_url_csv  /train  │
                        └──────┬────────────────────────┬──────────┘
                               │                        │
              ┌────────────────▼────┐     ┌────────────▼──────────────┐
              │  URL Feature        │     │   Training Pipeline        │
              │  Extractor          │     │                            │
              │  (url_feature_      │     │  Data Ingestion            │
              │   extraction.py)    │     │       ↓                    │
              │                     │     │  Data Validation           │
              │  Tier 1: URL parse  │     │       ↓                    │
              │  Tier 2: HTML fetch │     │  Data Transformation       │
              │  Tier 3: defaults   │     │       ↓                    │
              └────────┬────────────┘     │  Model Trainer             │
                       │                  │   (6 classifiers + CV)     │
              ┌────────▼────────────┐     └────────────┬──────────────┘
              │   NetworkModel      │                  │
              │  (preprocessor +   │◄─────────────────┘
              │   best_model.pkl)   │       best model saved
              └────────┬────────────┘
                       │
              ┌────────▼────────────┐     ┌─────────────────────────┐
              │   Prediction        │     │   MLflow + DagsHub      │
              │   SAFE / MALICIOUS  │     │   F1 / Precision /      │
              └─────────────────────┘     │   Recall tracked        │
                                          └─────────────────────────┘
```

---

## 🔬 Live Feature Extraction — How It Works

The biggest upgrade: you no longer need to pre-compute features. The engine does it live in 3 tiers:

```
URL Input → "https://example-login.xyz/paypal"
                │
      ┌─────────▼──────────────────────────────────────────┐
      │  TIER 1 — Pure string parsing   (16 features, ~0ms) │
      │  having_IP_Address, URL_Length, having_At_Symbol,   │
      │  double_slash_redirecting, Prefix_Suffix,           │
      │  having_Sub_Domain, HTTPS_token, port, ...          │
      └─────────┬──────────────────────────────────────────┘
                │
      ┌─────────▼──────────────────────────────────────────┐
      │  TIER 2 — Live HTML page fetch   (8 features, ~1s)  │
      │  SSLfinal_State, Favicon, Request_URL,              │
      │  URL_of_Anchor, Links_in_tags, SFH,                 │
      │  on_mouseover, RightClick, popUpWidnow,             │
      │  Iframe, Redirect                                   │
      └─────────┬──────────────────────────────────────────┘
                │
      ┌─────────▼──────────────────────────────────────────┐
      │  TIER 3 — Honest neutral defaults  (6 features)     │
      │  Domain_registeration_length → 0  (WHOIS, no API)  │
      │  age_of_domain               → 0  (WHOIS, no API)  │
      │  web_traffic                 → 0  (Alexa shutdown)  │
      │  Page_Rank                   → 0  (Google shutdown) │
      │  Links_pointing_to_page      → 0  (paid SEO APIs)  │
      │  Statistical_report          → 1  (assumed clean)   │
      └─────────────────────────────────────────────────────┘
                │
      ┌─────────▼──────────────────────────────────────────┐
      │  30-feature vector → preprocessor → model → result  │
      │             ✅ SAFE   or   🔴 MALICIOUS              │
      └─────────────────────────────────────────────────────┘
```

> **24 of 30 features are genuinely computed live.** The remaining 6 are set to neutral defaults — honestly documented, not silently faked.

---

## 🤖 ML Models

All 5 classifiers are trained with hyperparameter tuning via grid search. The best scorer wins and is saved.

| Model | Tuned Parameters |
|---|---|
| 🌲 **Random Forest** | `n_estimators`: 8, 16, 32, 128, 256 |
| 🌳 **Decision Tree** | `criterion`: gini / entropy / log_loss |
| 🚀 **Gradient Boosting** | `learning_rate`, `subsample`, `n_estimators` |
| 📈 **Logistic Regression** | Default (strong baseline) |
| ⚡ **AdaBoost** | `learning_rate`, `n_estimators` |

**Metrics tracked via MLflow:** F1 Score · Precision · Recall

**Preprocessing:** KNN Imputer (k=3, uniform weights) handles missing values before any model sees the data.

---

## 📁 Project Structure

```
MLops/
├── 📄 app.py                          # FastAPI server — all 4 endpoints
├── 📄 main.py                         # Run training pipeline standalone
├── 📄 push_data.py                    # Push raw CSV to MongoDB Atlas
│
├── 📂 networksecurity/
│   ├── 📂 components/
│   │   ├── data_ingestion.py          # MongoDB → train/test CSV split
│   │   ├── data_validation.py         # Schema check + drift report
│   │   ├── data_transformation.py     # KNN impute + numpy save
│   │   └── model_trainer.py           # Train 5 models, pick best, log MLflow
│   │
│   ├── 📂 pipeline/
│   │   └── training_pipeline.py       # Orchestrates all 4 components
│   │
│   ├── 📂 utlis/
│   │   ├── 📂 main_utlis/utlis.py     # save/load objects, evaluate_models
│   │   ├── 📂 ml_utlis/
│   │   │   ├── model/estimator.py     # NetworkModel wrapper class
│   │   │   └── metric/classification_metric.py
│   │   └── url_feature_extraction.py  # ⭐ Live 3-tier feature extractor
│   │
│   ├── 📂 entity/
│   │   ├── config_entity.py           # Pipeline config dataclasses
│   │   └── artifact_entity.py         # Artifact path dataclasses
│   │
│   ├── 📂 constant/training_pipeline/ # All pipeline constants
│   ├── 📂 cloud/s3_syncer.py          # AWS S3 model sync
│   ├── 📂 exception/exception.py      # Custom exception handler
│   └── 📂 logging/logger.py           # Centralized logging
│
├── 📂 templates/
│   ├── index.html                     # Full custom frontend dashboard
│   └── table.html                     # Prediction results table
│
├── 📂 final_model/
│   ├── model.pkl                      # Trained best classifier
│   └── preprocessor.pkl               # Fitted KNN imputer
│
├── 📂 data_schema/schema.yaml         # Column types & names
├── 📂 network_data/phisingData.csv    # Raw training dataset
├── 📂 prediction_output/              # Saved CSVs from predict runs
├── 📄 Dockerfile
├── 📄 requirements.txt
└── 📄 setup.py
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB Atlas account
- AWS account (for S3/ECR/EC2 deployment)
- Docker (optional)

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/MLops.git
cd MLops
pip install -r requirements.txt
pip install -e .
```

### 2. Configure Environment

```bash
# Create .env in project root
MONGODB_URL_KEY=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
```

### 3. Load Data into MongoDB

```bash
python push_data.py
```

### 4. Train the Model

```bash
# Option A — run standalone
python main.py

# Option B — trigger via API after starting the server
curl http://localhost:8000/train
```

### 5. Start the Server

```bash
python app.py
# → http://localhost:8000
```

---

## 🌐 API Reference

### `GET /`
Serves the full custom frontend dashboard (`index.html`).

---

### `GET /train`
Runs the complete training pipeline: ingest → validate → transform → train → save model.

```bash
curl http://localhost:8000/train
# Response: "Training is successful"
```

---

### `POST /predict`
Batch prediction from a **pre-built feature CSV** (30 columns matching `schema.yaml`). Fast — no feature extraction happens.

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@valid_data/test.csv"
# Response: HTML table with predicted_column appended
```

---

### `POST /predict_url` ⭐ New
Classify a **single raw URL** in real-time. Extracts all 24 live features on the fly.

```bash
curl -X POST http://localhost:8000/predict_url \
  -d "url=https://suspicious-login.xyz/paypal"

# Response JSON:
{
  "url": "https://suspicious-login.xyz/paypal",
  "prediction": "MALICIOUS",
  "features": {
    "having_IP_Address": 1,
    "URL_Length": -1,
    "Prefix_Suffix": -1,
    ...
  }
}
```

---

### `POST /predict_url_csv` ⭐ New
Batch-classify a **CSV of raw URLs** (one column: `url`). Runs live feature extraction on every row.

```bash
curl -X POST http://localhost:8000/predict_url_csv \
  -F "file=@my_urls.csv"
# Response: HTML table with features + prediction for each URL
# Saved to: prediction_output/url_batch_output.csv
```

> ⚠️ Slower than `/predict` because each row triggers a real HTTP fetch of the target page. That's intentional — not a bug.

---

## 📊 Dataset

| Property | Value |
|---|---|
| Source | UCI Phishing Websites Dataset |
| Storage | MongoDB Atlas (`KrishAI.NetworkData`) |
| Size | ~11,000 URLs |
| Features | 30 numerical (all int64) |
| Target | `Result`: **1** = Legitimate, **-1** = Phishing |
| Train / Test split | 80% / 20% |

Feature encoding convention:
- `1` = Legitimate signal
- `0` = Neutral / unknown
- `-1` = Phishing / suspicious signal

---

## ☁️ Deployment

### Docker

```bash
docker build -t netguard .
docker run -d -p 8000:8000 \
  -e MONGODB_URL_KEY=your_connection_string \
  netguard
```

### AWS CI/CD via GitHub Actions

The pipeline runs automatically on every push to `main`:

```
git push → main
    │
    ▼
[1] Continuous Integration
    └── Lint & unit test checks
    │
    ▼
[2] Continuous Delivery
    ├── Configure AWS credentials
    ├── Login to Amazon ECR
    └── Build & push Docker image → ECR
    │
    ▼
[3] Continuous Deployment  (self-hosted EC2 runner)
    ├── Pull latest image from ECR
    ├── Run container on port 8080
    └── Prune old images
```

#### Required GitHub Secrets

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `AWS_ECR_LOGIN_URI` | e.g. `788614365622.dkr.ecr.us-east-1.amazonaws.com/netguard` |
| `ECR_REPOSITORY_NAME` | e.g. `netguard` |

#### EC2 Docker Setup (run once on fresh instance)

```bash
sudo apt-get update -y && sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

#### S3 Bucket

Model artifacts are synced to S3 bucket: `netguard-harsh-mlops`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10 |
| **ML** | scikit-learn (5 classifiers + GridSearchCV) |
| **API** | FastAPI + Uvicorn |
| **Frontend** | Jinja2 HTML templates |
| **Database** | MongoDB Atlas (via PyMongo) |
| **Feature Extraction** | requests + BeautifulSoup4 |
| **Experiment Tracking** | MLflow + DagsHub |
| **Cloud** | AWS S3, EC2, ECR |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Serialization** | dill (model/preprocessor pkl) |

---

## 📈 MLflow Metrics Tracked

Every training run logs to DagsHub:

```
Run: random_forest_20240916
├── f1_score:        0.974
├── precision:       0.981
└── recall_score:    0.968
```

---

<div align="center">

**⭐ Star this repo if you found it useful!**

Made with 🛡️ | NetGuard · Phishing Detection · MLOps · Real-Time URL Analysis

</div>
