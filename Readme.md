<!-- Header Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0d0d,50:0a192f,100:112240&height=220&section=header&text=NetGuard%20MLOps&fontSize=54&fontColor=64ffda&fontAlignY=38&desc=Phishing%20URL%20Detection%20%7C%20Real-Time%20Feature%20Extraction%20%7C%20CI%2FCD%20to%20AWS&descAlignY=60&descColor=8892b0" width="100%"/>

<div align="center">

<!-- Badges -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>
  <img src="https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>
</p>
<p>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS-EC2%20%7C%20ECR%20%7C%20S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/DagsHub-Experiment%20Tracking-FF6B35?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-64ffda?style=for-the-badge"/>
</p>

<br/>

> **Type a raw URL. Get an instant phishing verdict.**
> Live HTML scraping · Ensemble ML · Automated CI/CD to AWS.

<br/>

[🚀 Quick Start](#-quick-start) · [🏗️ Architecture](#%EF%B8%8F-architecture) · [🔬 Feature Engine](#-live-feature-extraction) · [🌐 API](#-api-reference) · [🤖 ML Models](#-ml-models) · [☁️ Deploy](#%EF%B8%8F-deployment)

</div>

---

## 📌 Table of Contents

- [What's New](#-whats-new-in-this-version)
- [Overview](#-overview)
- [Architecture](#%EF%B8%8F-architecture)
- [Live Feature Extraction](#-live-feature-extraction)
- [ML Models](#-ml-models)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Dataset](#-dataset)
- [Getting Started](#-quick-start)
- [Deployment](#%EF%B8%8F-deployment)
- [Tech Stack](#%EF%B8%8F-tech-stack)
- [Skills Demonstrated](#-skills-demonstrated)

---

## 🆕 What's New in This Version

| Feature | Previous Version | This Version |
|---|---|---|
| 🔴 **Live URL Scan** | ❌ Not supported | ✅ Type any raw URL → instant verdict |
| ⚙️ **Feature Extraction** | Manual / pre-built CSVs | ✅ 24/30 features extracted live |
| 🌐 **API Endpoints** | 2 (`/train`, `/predict`) | ✅ 4 endpoints including 2 new URL routes |
| 🖥️ **Frontend** | Bare Swagger UI | ✅ Full custom HTML dashboard |
| 📦 **Batch URL Mode** | Feature CSVs only | ✅ Raw URL CSVs — auto-extract & classify |
| 🕸️ **HTML Scraping** | ❌ None | ✅ BeautifulSoup4 live page analysis |

---

## 🌐 Overview

**NetGuard** is a production-ready, end-to-end MLOps system that detects phishing URLs using 30 URL and network-behavioural features. It ingests raw data from MongoDB Atlas, runs it through a fully automated ML training pipeline, and exposes a FastAPI service that can classify URLs in real time — no pre-built feature vectors needed.

### 🎯 What This Project Covers

| Domain | What's Built |
|---|---|
| 🏗️ **MLOps Pipeline** | Automated ingestion → validation → transformation → training |
| 🔬 **Feature Engineering** | Live 3-tier URL feature extraction engine |
| 🤖 **ML Training** | 5 classifiers with hyperparameter grid search |
| 🌐 **REST API** | FastAPI with 4 endpoints + custom HTML frontend |
| 📊 **Experiment Tracking** | MLflow + DagsHub — F1, Precision, Recall |
| ☁️ **Cloud Deployment** | Docker → AWS ECR → EC2 via GitHub Actions CI/CD |

---

## 🏛️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                           │
│          Browser UI  │   REST API   │   CSV Upload               │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│                                                                  │
│   GET  /          → Custom HTML Dashboard                        │
│   GET  /train     → Trigger Training Pipeline                    │
│   POST /predict          → Batch (pre-built feature CSV)         │
│   POST /predict_url      → Single raw URL  ⭐ NEW                │
│   POST /predict_url_csv  → Bulk raw URLs   ⭐ NEW                │
└───────────┬──────────────────────────────────────┬───────────────┘
            │                                      │
            ▼                                      ▼
┌───────────────────────┐            ┌─────────────────────────────┐
│   URL Feature         │            │      Training Pipeline       │
│   Extractor           │            │                              │
│                       │            │  [1] Data Ingestion          │
│   Tier 1 · URL parse  │            │       MongoDB → CSV split    │
│   Tier 2 · HTML fetch │            │                              │
│   Tier 3 · defaults   │            │  [2] Data Validation         │
│                       │            │       Schema + drift report  │
│   24/30 live features │            │                              │
└───────────┬───────────┘            │  [3] Data Transformation     │
            │                        │       KNN Imputer + .npy     │
            ▼                        │                              │
┌───────────────────────┐            │  [4] Model Trainer           │
│     NetworkModel      │◄───────────│       5 classifiers + CV     │
│   preprocessor.pkl    │            │       Best model saved       │
│   +  model.pkl        │            └─────────────────────────────┘
└───────────┬───────────┘
            │                        ┌─────────────────────────────┐
            ▼                        │   MLflow + DagsHub          │
  ✅ SAFE / 🔴 MALICIOUS             │   F1 · Precision · Recall   │
  + full feature breakdown           └─────────────────────────────┘
```

---

## 🔬 Live Feature Extraction

The biggest upgrade over v1 — you no longer need to pre-compute features. The engine handles it live in 3 tiers:

```
Raw URL Input  →  "https://paypal-login.free.xyz/secure/verify"
      │
      │
      ├──── TIER 1  ·  Pure String Parsing  ·  ~0ms  ·  16 features
      │     ┌─────────────────────────────────────────────────────┐
      │     │  having_IP_Address       URL_Length                 │
      │     │  Shortining_Service      having_At_Symbol           │
      │     │  double_slash_redirect   Prefix_Suffix              │
      │     │  having_Sub_Domain       HTTPS_token                │
      │     │  port  ...                                          │
      │     └─────────────────────────────────────────────────────┘
      │
      ├──── TIER 2  ·  Live HTML Page Fetch  ·  ~1s  ·  8 features
      │     ┌─────────────────────────────────────────────────────┐
      │     │  SSLfinal_State   Favicon       Request_URL         │
      │     │  URL_of_Anchor    Links_in_tags SFH                 │
      │     │  on_mouseover     RightClick    popUpWidnow         │
      │     │  Iframe           Redirect                          │
      │     └─────────────────────────────────────────────────────┘
      │
      └──── TIER 3  ·  Honest Neutral Defaults  ·  6 features
            ┌─────────────────────────────────────────────────────┐
            │  Domain_registeration_length → 0  (WHOIS, no API)  │
            │  age_of_domain               → 0  (WHOIS, no API)  │
            │  web_traffic                 → 0  (Alexa shutdown)  │
            │  Page_Rank                   → 0  (Google shutdown) │
            │  Links_pointing_to_page      → 0  (paid SEO APIs)  │
            │  Statistical_report          → 1  (clean by default)│
            └─────────────────────────────────────────────────────┘
                               │
                               ▼
            30-feature vector → preprocessor → model
                               │
                     ✅ SAFE  or  🔴 MALICIOUS
```

> **24 of 30 features are genuinely computed live.** The remaining 6 use honest neutral defaults — documented transparently, never silently faked.

---

## 🤖 ML Models

5 classifiers compete with hyperparameter grid search. The best F1 scorer is saved automatically.

| Model | Hyperparameters Tuned |
|---|---|
| 🌲 **Random Forest** | `n_estimators`: 8 · 16 · 32 · 128 · 256 |
| 🌳 **Decision Tree** | `criterion`: gini · entropy · log_loss |
| 🚀 **Gradient Boosting** | `learning_rate`, `subsample`, `n_estimators` |
| 📈 **Logistic Regression** | Strong baseline — no tuning needed |
| ⚡ **AdaBoost** | `learning_rate`, `n_estimators` |

**Preprocessing:** KNN Imputer (k=3, uniform weights) handles missing values before any model sees the data.

**MLflow tracks every run:**

```
Run: gradient_boosting_20240625
├── f1_score:        0.974
├── precision:       0.981
└── recall_score:    0.968
```

---

## 📁 Project Structure

```
MLops/
│
├── 📄 app.py                              # FastAPI — all 4 prediction endpoints
├── 📄 main.py                             # Run training pipeline standalone
├── 📄 push_data.py                        # Push CSV → MongoDB Atlas
│
├── 📂 networksecurity/
│   ├── 📂 components/
│   │   ├── data_ingestion.py              # MongoDB → train/test CSV split
│   │   ├── data_validation.py             # Schema check + drift report
│   │   ├── data_transformation.py         # KNN impute + .npy save
│   │   └── model_trainer.py               # Train 5 models, pick best, log MLflow
│   │
│   ├── 📂 pipeline/
│   │   └── training_pipeline.py           # Orchestrates all 4 components
│   │
│   ├── 📂 utlis/
│   │   ├── main_utlis/utlis.py            # save/load objects, evaluate_models
│   │   ├── ml_utlis/
│   │   │   ├── model/estimator.py         # NetworkModel wrapper class
│   │   │   └── metric/classification_metric.py
│   │   └── url_feature_extraction.py      # ⭐ Live 3-tier feature extractor
│   │
│   ├── 📂 entity/
│   │   ├── config_entity.py               # Pipeline config dataclasses
│   │   └── artifact_entity.py             # Artifact path dataclasses
│   │
│   ├── 📂 constant/training_pipeline/     # All pipeline constants
│   ├── 📂 cloud/s3_syncer.py              # AWS S3 model sync
│   ├── 📂 exception/exception.py          # Custom exception handler
│   └── 📂 logging/logger.py              # Centralized logging
│
├── 📂 templates/
│   ├── index.html                         # Custom frontend dashboard
│   └── table.html                         # Prediction results renderer
│
├── 📂 final_model/
│   ├── model.pkl                          # Best trained classifier
│   └── preprocessor.pkl                   # Fitted KNN imputer
│
├── 📂 data_schema/schema.yaml             # Column types & feature order
├── 📂 network_data/phisingData.csv        # Raw training dataset (~11k URLs)
├── 📂 prediction_output/                  # Saved CSVs from prediction runs
│   ├── output.csv                         # /predict results
│   └── url_batch_output.csv              # /predict_url_csv results
│
├── 📄 Dockerfile
├── 📄 requirements.txt
└── 📄 setup.py
```

---

## 🌐 API Reference

### `GET /`
Serves the full custom frontend dashboard.

---

### `GET /train`
Triggers the complete training pipeline — ingest → validate → transform → train → save model.

```bash
curl http://localhost:8000/train
# → "Training is successful"
```

---

### `POST /predict`
Batch prediction from a **pre-built feature CSV** (30 columns matching schema). No feature extraction — fast.

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@valid_data/test.csv"
# → HTML table with predicted_column appended
```

---

### `POST /predict_url` ⭐ New
Classify a **single raw URL** with live feature extraction.

```bash
curl -X POST http://localhost:8000/predict_url \
  -d "url=https://suspicious-login.xyz/paypal"
```

```json
{
  "url": "https://suspicious-login.xyz/paypal",
  "prediction": "MALICIOUS",
  "features": {
    "having_IP_Address": 1,
    "URL_Length": -1,
    "Prefix_Suffix": -1,
    "SSLfinal_State": -1,
    "Favicon": -1,
    "..."
  }
}
```

---

### `POST /predict_url_csv` ⭐ New
Bulk-classify a **CSV of raw URLs** (one column: `url`). Runs live extraction on every row.

```bash
curl -X POST http://localhost:8000/predict_url_csv \
  -F "file=@my_urls.csv"
# → HTML table · saved to prediction_output/url_batch_output.csv
```

> ⚠️ Slower than `/predict` because each row triggers a real HTTP page fetch. That's the honest tradeoff for not needing pre-built features.

---

## 📊 Dataset

| Property | Value |
|---|---|
| **Source** | UCI Phishing Websites Dataset |
| **Storage** | MongoDB Atlas — `KrishAI.NetworkData` |
| **Size** | ~11,000 URLs |
| **Features** | 30 numerical (all `int64`) |
| **Target** | `Result`: **1** = Legitimate · **-1** = Phishing |
| **Train / Test Split** | 80% / 20% |

**Feature encoding convention:**

| Value | Meaning |
|---|---|
| `1` | Legitimate / safe signal |
| `0` | Neutral / unknown |
| `-1` | Phishing / suspicious signal |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- MongoDB Atlas account
- AWS account (for cloud deployment)
- Docker (optional)

### 1. Clone & Install

```bash
git clone https://github.com/HarshMaurya14/networksecurity.git
cd networksecurity
pip install -r requirements.txt
pip install -e .
```

### 2. Configure Environment

```env
# .env
MONGODB_URL_KEY=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
```

### 3. Push Data to MongoDB

```bash
python push_data.py
```

### 4. Run the Training Pipeline

```bash
# Option A — standalone script
python main.py

# Option B — via API after server starts
curl http://localhost:8000/train
```

### 5. Launch the Server

```bash
python app.py
# → http://localhost:8000
```

---

## ☁️ Deployment

### Docker

```bash
docker build -t netguard .

docker run -d -p 8000:8000 \
  -e MONGODB_URL_KEY=your_connection_string \
  netguard
```

### GitHub Actions CI/CD Pipeline

```
git push → main
      │
      ▼
┌─────────────────────────────┐
│  [1] Continuous Integration │  ← Lint & unit test checks
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  [2] Continuous Delivery    │  ← Build Docker image → push to AWS ECR
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  [3] Continuous Deployment  │  ← Pull & run on EC2 (self-hosted runner)
└─────────────────────────────┘
```

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `AWS_ECR_LOGIN_URI` | Your ECR registry URI |
| `ECR_REPOSITORY_NAME` | Your ECR repository name |

### EC2 Docker Setup (run once on fresh instance)

```bash
sudo apt-get update -y && sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu && newgrp docker
```

**S3 bucket for model artifacts:** `netguard-harsh-mlops`

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Language** | Python 3.10 |
| **ML Framework** | scikit-learn — 5 classifiers + GridSearchCV |
| **API** | FastAPI + Uvicorn |
| **Frontend** | Jinja2 HTML templates |
| **Database** | MongoDB Atlas (PyMongo) |
| **Feature Extraction** | requests + BeautifulSoup4 |
| **Experiment Tracking** | MLflow + DagsHub |
| **Cloud** | AWS S3 · EC2 · ECR |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Serialization** | dill (.pkl model files) |

</div>

---

## 🎓 Skills Demonstrated

- ✅ **MLOps** — end-to-end automated ML pipeline design
- ✅ **Feature Engineering** — live 3-tier URL feature extraction from raw HTML
- ✅ **Model Selection** — multi-model training with grid search and auto-selection
- ✅ **API Development** — FastAPI with multiple prediction modes
- ✅ **Experiment Tracking** — MLflow + DagsHub integration
- ✅ **Cloud Deployment** — Docker → ECR → EC2 with full CI/CD
- ✅ **Data Engineering** — MongoDB ingestion, validation, transformation pipeline

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

**⭐ Star this repo if you found it useful!**

Made with ❤️ by [Harsh Maurya](https://github.com/HarshMaurya14)

All implementation done independently by me.

</div>

<!-- Footer Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0d0d,50:0a192f,100:112240&height=120&section=footer" width="100%"/>
