<!-- Header Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0d0d,50:0a192f,100:112240&height=220&section=header&text=NetGuard%20MLOps&fontSize=54&fontColor=64ffda&fontAlignY=38&desc=Phishing%20URL%20Detection%20%7C%20Real-Time%20Feature%20Extraction%20%7C%20CI%2FCD%20to%20AWS&descAlignY=60&descColor=8892b0" width="100%"/>

<div align="center">

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

[🚀 Quick Start](#-quick-start) · [🏗️ Architecture](#%EF%B8%8F-system-architecture) · [🔬 Feature Engine](#-live-feature-extraction) · [🌐 API](#-api-reference) · [🤖 ML Models](#-ml-models) · [☁️ Deploy](#%EF%B8%8F-deployment)

</div>

🎥 Demo Video: [https://youtu.be/your-video](https://youtu.be/uarEXG4vUUA)

---

## 📌 Table of Contents

- [What's New](#-whats-new-in-this-version)
- [Overview](#-overview)
- [System Architecture](#%EF%B8%8F-system-architecture)
- [ETL Pipeline](#-etl-pipeline)
- [Training Pipeline — Deep Dive](#-training-pipeline--deep-dive)
- [Live Feature Extraction](#-live-feature-extraction)
- [ML Models](#-ml-models)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Dataset](#-dataset)
- [Quick Start](#-quick-start)
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
| 🤖 **ML Training** | 5 classifiers with hyperparameter grid search + auto model selection |
| 🌐 **REST API** | FastAPI with 4 prediction endpoints + custom HTML frontend |
| 📊 **Experiment Tracking** | MLflow + DagsHub — F1, Precision, Recall per run |
| ☁️ **Cloud Deployment** | Docker → AWS ECR → EC2 via GitHub Actions CI/CD |

---

## 🏛️ System Architecture

```
╔══════════════════════════════════════════════════════════════════════╗
║                         DATA SOURCES                                ║
║   📂 Local CSV Dataset        🌐 APIs / S3 / Internal DBs           ║
╚══════════════════════════════╦═══════════════════════════════════════╝
                               ║
                               ▼
╔══════════════════════════════════════════════════════════════════════╗
║                       ETL PIPELINE                                  ║
║                                                                     ║
║   CSV Rows  ──►  JSON Transform  ──►  MongoDB Atlas                 ║
║   {A:100, B:120, C:140}                    
╚══════════════════════════════╦═══════════════════════════════════════╝
                               ║
                               ▼
╔══════════════════════════════════════════════════════════════════════╗
║                    TRAINING PIPELINE                                ║
║                                                                     ║
║  ┌─────────────────┐   ┌─────────────────┐   ┌──────────────────┐  ║
║  │ Data Ingestion  │──►│ Data Validation │──►│ Data Transform.  │  ║
║  │                 │   │                 │   │                  │  ║
║  │ MongoDB → CSV   │   │ Schema check    │   │ KNN Imputer      │  ║
║  │ 80/20 split     │   │ Drift report    │   │ SMOTETomek       │  ║
║  │ Drop columns    │   │ Col validation  │   │ → train/test.npy │  ║
║  └─────────────────┘   └─────────────────┘   └──────────────────┘  ║
║                                                        ║            ║
║                                                        ▼            ║
║  ┌─────────────────┐   ┌─────────────────┐   ┌──────────────────┐  ║
║  │  Model Pusher   │◄──│ Model Evaluator │◄──│  Model Trainer   │  ║
║  │                 │   │                 │   │                  │  ║
║  │ Model Accepted? │   │ vs base score   │   │ 5 classifiers    │  ║
║  │ Yes → Cloud     │   │ F1/Prec/Recall  │   │ Grid search CV   │  ║
║  │ No  → None      │   │ metric artifact │   │ Best model saved │  ║
║  └─────────────────┘   └─────────────────┘   └──────────────────┘  ║
╚══════════════════════════════╦═══════════════════════════════════════╝
                               ║
                               ▼
╔══════════════════════════════════════════════════════════════════════╗
║                      FastAPI APPLICATION                            ║
║                                                                     ║
║   GET  /               → Custom HTML Dashboard                      ║
║   GET  /train          → Trigger Training Pipeline                  ║
║   POST /predict        → Batch (pre-built 30-feature CSV)           ║
║   POST /predict_url    → Single raw URL  ⭐ NEW                     ║
║   POST /predict_url_csv → Bulk raw URLs  ⭐ NEW                     ║
╚══════════════════════════════╦═══════════════════════════════════════╝
                               ║
               ┌───────────────╩────────────────┐
               ▼                                ▼
╔══════════════════════╗            ╔═══════════════════════╗
║   URL Feature        ║            ║  NetworkModel         ║
║   Extractor          ║            ║                       ║
║                      ║            ║  preprocessor.pkl     ║
║  Tier 1: URL parse   ║──────────►║  +  model.pkl         ║
║  Tier 2: HTML fetch  ║            ║                       ║
║  Tier 3: defaults    ║            ║  → SAFE / MALICIOUS   ║
╚══════════════════════╝            ╚═══════════════════════╝
```

---

## 🔄 ETL Pipeline

The raw CSV dataset is transformed to JSON and pushed to MongoDB Atlas before training begins.

```
  EXTRACT                  TRANSFORM                   LOAD
┌──────────────┐          ┌─────────────────┐        ┌──────────────────┐
│   Source     │          │  Basic Preproc  │        │  Destination     │
│              │          │                 │        │                  │
│  Local CSV   │ ───────► │  Cleaning raw   │ ─────► │  MongoDB Atlas   │
│  Dataset     │          │  data           │        │  AWS DynamoDB    │
│              │          │                 │        │  MySQL           │
│  APIs        │          │  CSV row:       │        │  S3 Buckets      │
│  S3 Buckets  │          │  {A:100,        │        │                  │
│  Paid APIs   │          │   B:120,        │        └──────────────────┘
│  Internal DB │          │   C:140}        │
└──────────────┘          │       ↓         │
                          │    JSON array   │
                          │  pushed to DB   │
                          └─────────────────┘
```

---

## 🔬 Training Pipeline — Deep Dive

### Step 1 — Data Ingestion

```
MongoDB Atlas (KrishAI.NetworkData)
         │
         ▼  ① Fetch collection
┌────────────────────┐
│ Data Ingestion     │◄── Config: dir paths, collection name,
│ Component          │            train/test split ratio
└────────┬───────────┘
         │  ② Export to Feature Store  →  raw.csv (timestamped)
         │  ③ Drop unwanted columns
         │  ④ Split 80/20             →  train.csv + test.csv
         ▼
   Data Ingestion Artifact
   (paths to train.csv, test.csv)
```

### Step 2 — Data Validation

```
      train.csv + test.csv
              │
              ▼
┌──────────────────────────────┐
│  Data Validation Component   │◄── Schema: 30 features, int64
│                              │
│  ① Same schema?              │──── ✅ Same no. of features
│  ② Numerical columns exist?  │──── ✅ Datatype validated
│  ③ Data drift detected?      │──── 📊 Drift report generated
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
  valid_train.csv   Drift Report
  valid_test.csv    (YAML artifact)
```

### Step 3 — Data Transformation

```
  valid_train.csv + valid_test.csv
              │
              ▼
┌──────────────────────────────────┐
│  Data Transformation Component   │
│                                  │
│  ① Drop target column            │
│  ② KNN Imputer (k=3, uniform)   │◄── handles missing values
│  ③ SMOTETomek                    │◄── balances class distribution
│  ④ fit_transform on train        │
│     transform on test            │
│  ⑤ Save preprocessor.pkl        │
└──────────────┬───────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
   train.npy        test.npy
   (numpy arrays, ready for training)
```

### Step 4 — Model Trainer

```
  train.npy + test.npy + preprocessor.pkl
              │
              ▼
┌──────────────────────────────────┐
│  Model Trainer Component         │
│                                  │
│  Model Factory → get_best_model  │
│                                  │
│  ┌───────────────────────────┐   │
│  │  5 Classifiers compete:   │   │
│  │  • Random Forest          │   │
│  │  • Decision Tree          │   │
│  │  • Gradient Boosting      │   │
│  │  • Logistic Regression    │   │
│  │  • AdaBoost               │   │
│  └───────────────────────────┘   │
│                                  │
│  best_score ≥ expected_accuracy? │
│  ✅ Yes → Save NetworkModel      │
│  ❌ No  → Raise exception        │
└──────────────┬───────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
   model.pkl       metric_artifact
   (NetworkModel)  (F1, Precision, Recall)
                   → logged to MLflow + DagsHub
```

### Step 5 — Model Evaluation & Pusher

```
  model.pkl + metric_artifact
              │
              ▼
┌──────────────────────────────────┐
│  Model Evaluator                 │
│                                  │
│  New model score vs base score?  │
│                                  │
│  ✅ Accepted → Model Pusher      │──► Cloud (AWS S3 / Azure)
│  ❌ Rejected → None              │
└──────────────────────────────────┘
```

---

## 🔬 Live Feature Extraction

```
Raw URL Input → "https://paypal-login.free.xyz/secure/verify"
      │
      ├── TIER 1 · Pure string parsing · ~0ms · 16 features
      │   ┌──────────────────────────────────────────────────┐
      │   │  having_IP_Address       URL_Length              │
      │   │  Shortining_Service      having_At_Symbol        │
      │   │  double_slash_redirect   Prefix_Suffix           │
      │   │  having_Sub_Domain       HTTPS_token  · port ... │
      │   └──────────────────────────────────────────────────┘
      │
      ├── TIER 2 · Live HTML page fetch · ~1s · 8 features
      │   ┌──────────────────────────────────────────────────┐
      │   │  SSLfinal_State   Favicon      Request_URL       │
      │   │  URL_of_Anchor    Links_in_tags   SFH            │
      │   │  on_mouseover     RightClick   popUpWidnow       │
      │   │  Iframe           Redirect                       │
      │   └──────────────────────────────────────────────────┘
      │
      └── TIER 3 · Honest neutral defaults · 6 features
          ┌──────────────────────────────────────────────────┐
          │  Domain_registeration_length → 0 (no WHOIS API) │
          │  age_of_domain               → 0 (no WHOIS API) │
          │  web_traffic                 → 0 (Alexa down)   │
          │  Page_Rank                   → 0 (Google down)  │
          │  Links_pointing_to_page      → 0 (paid APIs)    │
          │  Statistical_report          → 1 (default safe) │
          └──────────────────────────────────────────────────┘
                             │
                             ▼
          30-feature vector → preprocessor → model
                             │
                   ✅ SAFE  or  🔴 MALICIOUS
```

> **24 of 30 features computed live.** The remaining 6 use honest neutral defaults — never silently faked.

---

## 🤖 ML Models

| Model | Hyperparameters Tuned |
|---|---|
| 🌲 **Random Forest** | `n_estimators`: 8 · 16 · 32 · 128 · 256 |
| 🌳 **Decision Tree** | `criterion`: gini · entropy · log_loss |
| 🚀 **Gradient Boosting** | `learning_rate`, `subsample`, `n_estimators` |
| 📈 **Logistic Regression** | Strong baseline |
| ⚡ **AdaBoost** | `learning_rate`, `n_estimators` |

MLflow tracks every run: `f1_score` · `precision` · `recall_score`

---

## 📁 Project Structure

```
MLops/
│
├── 📄 app.py                              # FastAPI — all 4 endpoints
├── 📄 main.py                             # Run training pipeline standalone
├── 📄 push_data.py                        # Push CSV → MongoDB Atlas
│
├── 📂 networksecurity/
│   ├── 📂 components/
│   │   ├── data_ingestion.py              # MongoDB → train/test split
│   │   ├── data_validation.py             # Schema check + drift report
│   │   ├── data_transformation.py         # KNN impute + SMOTETomek + .npy
│   │   └── model_trainer.py               # Train 5 models, pick best, log MLflow
│   │
│   ├── 📂 pipeline/
│   │   └── training_pipeline.py           # Orchestrates all components
│   │
│   ├── 📂 utlis/
│   │   ├── main_utlis/utlis.py            # save/load objects, evaluate_models
│   │   ├── ml_utlis/model/estimator.py    # NetworkModel wrapper
│   │   └── url_feature_extraction.py      # ⭐ Live 3-tier feature extractor
│   │
│   ├── 📂 entity/                         # Config & artifact dataclasses
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
├── 📂 data_schema/schema.yaml
├── 📂 network_data/phisingData.csv
├── 📂 prediction_output/
├── 📄 Dockerfile
├── 📄 requirements.txt
└── 📄 setup.py
```

---

## 🌐 API Reference

### `GET /train`
Triggers the full pipeline: ingest → validate → transform → train → save.

```bash
curl http://localhost:8000/train
```

### `POST /predict`
Batch prediction from a **pre-built 30-feature CSV**. Fast — no extraction.

```bash
curl -X POST http://localhost:8000/predict -F "file=@valid_data/test.csv"
```

### `POST /predict_url` ⭐ New
Single raw URL classified with live feature extraction.

```bash
curl -X POST http://localhost:8000/predict_url \
  -d "url=https://suspicious-login.xyz/paypal"
```

```json
{
  "url": "https://suspicious-login.xyz/paypal",
  "prediction": "MALICIOUS",
  "features": { "having_IP_Address": 1, "URL_Length": -1, "..." }
}
```

### `POST /predict_url_csv` ⭐ New
CSV of raw URLs (column: `url`) — live extraction on every row.

```bash
curl -X POST http://localhost:8000/predict_url_csv -F "file=@my_urls.csv"
```

---

## 📊 Dataset

| Property | Value |
|---|---|
| **Source** | UCI Phishing Websites Dataset |
| **Storage** | MongoDB Atlas — `KrishAI.NetworkData` |
| **Size** | ~11,000 URLs |
| **Features** | 30 numerical (`int64`) |
| **Target** | `Result`: **1** = Legitimate · **-1** = Phishing |
| **Split** | 80% train / 20% test |

---

## 🚀 Quick Start

```bash
# 1. Clone & install
git clone https://github.com/HarshMaurya14/networksecurity.git
cd networksecurity
pip install -r requirements.txt && pip install -e .

# 2. Set environment variable
export MONGODB_URL_KEY="mongodb+srv://<user>:<pass>@cluster.mongodb.net/"

# 3. Push data to MongoDB
python push_data.py

# 4. Train
python main.py

# 5. Serve
python app.py   # → http://localhost:8000
```

---

## ☁️ Deployment

### CI/CD Flow — GitHub Actions

```
git push → main branch
      │
      ▼
╔══════════════════════════════════════════════════════════╗
║  STEP 1 — Continuous Integration                        ║
║  • Lint checks                                          ║
║  • Unit tests                                           ║
╚══════════════════════════╦═══════════════════════════════╝
                           ║
                           ▼
╔══════════════════════════════════════════════════════════╗
║  STEP 2 — Continuous Delivery                           ║
║  • Configure AWS credentials                            ║
║  • Login to Amazon ECR                                  ║
║  • docker build -t netguard .                           ║
║  • docker push → AWS ECR Registry                       ║
╚══════════════════════════╦═══════════════════════════════╝
                           ║
                           ▼
╔══════════════════════════════════════════════════════════╗
║  STEP 3 — Continuous Deployment  (self-hosted EC2)      ║
║  • docker pull latest image from ECR                    ║
║  • docker run -d -p 8080:8000 netguard                  ║
║  • docker system prune (clean old images)               ║
╚══════════════════════════════════════════════════════════╝
                           ║
                           ▼
                    🌐 Live on EC2
               http://<ec2-ip>:8080
```

### Deployment Flow (from your notes)

```
┌──────────────────┐        ┌───────────────┐        ┌────────────┐
│ Network Security │ ──①──► │   AWS ECR     │ ──────► │  AWS EC2   │
│   (Source Code)  │        │ Docker Image  │        │  Running   │
└──────────────────┘        └───────────────┘        └────────────┘
                                    ▲
                             ②  GitHub Actions
                             CI → CD Pipeline
                                    │
                               App Runner
```

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `AWS_ECR_LOGIN_URI` | Your ECR registry URI |
| `ECR_REPOSITORY_NAME` | Your ECR repo name |

### EC2 Docker Setup

```bash
sudo apt-get update -y && sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu && newgrp docker
```

### Docker

```bash
docker build -t netguard .
docker run -d -p 8000:8000 -e MONGODB_URL_KEY=your_url netguard
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Language** | Python 3.10 |
| **ML** | scikit-learn — 5 classifiers + GridSearchCV |
| **Imbalance Handling** | SMOTETomek (imblearn) |
| **API** | FastAPI + Uvicorn |
| **Frontend** | Jinja2 HTML templates |
| **Database** | MongoDB Atlas (PyMongo) |
| **Feature Extraction** | requests + BeautifulSoup4 |
| **Experiment Tracking** | MLflow + DagsHub |
| **Cloud** | AWS S3 · EC2 · ECR |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Serialization** | dill (.pkl files) |

</div>

---

## 🎓 Skills Demonstrated

- ✅ **MLOps** — end-to-end automated ML pipeline design
- ✅ **ETL Engineering** — CSV → JSON → MongoDB ingestion pipeline
- ✅ **Feature Engineering** — live 3-tier URL feature extraction from raw HTML
- ✅ **Model Selection** — multi-model grid search with automated best-model selection
- ✅ **Class Imbalance** — SMOTETomek oversampling + undersampling
- ✅ **API Development** — FastAPI with multiple prediction modes
- ✅ **Experiment Tracking** — MLflow + DagsHub integration
- ✅ **Cloud Deployment** — Docker → ECR → EC2 with full CI/CD

---

<div align="center">

**⭐ Star this repo if you found it useful!**

Made with ❤️ by [Harsh Maurya](https://github.com/HarshMaurya14)

All implementation done independently by me.

</div>

<!-- Footer Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0d0d,50:0a192f,100:112240&height=120&section=footer" width="100%"/>
