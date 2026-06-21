import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Form
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utlis.main_utlis.utlis import load_object

from networksecurity.utlis.ml_utlis.model.estimator import NetworkModel
from networksecurity.utlis.url_feature_extraction import extract_features


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    """
    Bulk prediction from a CSV that already has all 30 pre-built
    features (same format as the training data). No feature
    extraction happens here — it assumes the numbers are already
    computed and just runs them through the model.
    """
    try:
        try:
            df = pd.read_csv(file.file, encoding="utf-8")
        except UnicodeDecodeError:
            file.file.seek(0)
            df = pd.read_csv(file.file, encoding="latin-1")

        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor, model=final_model)

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred

        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped', index=False)

        return templates.TemplateResponse(
            request=request, name="table.html", context={"table": table_html}
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict_url")
async def predict_url_route(request: Request, url: str = Form(...)):
    """
    Single raw URL classification. Computes all 30 features live
    (24 genuinely extracted, 6 honest neutral defaults for features
    that need now-defunct/paid services) and returns the verdict
    plus the full feature breakdown.
    """
    try:
        features = extract_features(url)
        input_df = pd.DataFrame([features])

        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor, model=final_model)

        y_pred = network_model.predict(input_df)
        result = "SAFE" if y_pred[0] == 1 else "MALICIOUS"

        return {
            "url": url,
            "prediction": result,
            "features": features,
        }

    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict_url_csv")
async def predict_url_csv_route(request: Request, file: UploadFile = File(...)):
    """
    Bulk prediction from a CSV of RAW URLs (one column, e.g. "url").
    Runs the same live feature extraction used by /predict_url on
    every row, then classifies each one. Slower than /predict since
    every row triggers a real HTTP fetch of the target page — that's
    an honest tradeoff, not a bug.
    """
    try:
        try:
            df = pd.read_csv(file.file, encoding="utf-8")
        except UnicodeDecodeError:
            file.file.seek(0)
            df = pd.read_csv(file.file, encoding="latin-1")

        url_col = "url" if "url" in df.columns else df.columns[0]

        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor, model=final_model)

        rows = []
        for raw_url in df[url_col].astype(str):
            try:
                features = extract_features(raw_url)
                input_df = pd.DataFrame([features])
                y_pred = network_model.predict(input_df)
                result = "SAFE" if y_pred[0] == 1 else "MALICIOUS"
            except Exception:
                features = {}
                result = "ERROR"

            row = {"url": raw_url, **features, "predicted_column": result}
            rows.append(row)

        result_df = pd.DataFrame(rows)
        result_df.to_csv("prediction_output/url_batch_output.csv", index=False)

        table_html = result_df.to_html(classes="table table-striped", index=False)
        return templates.TemplateResponse(
            request=request, name="table.html", context={"table": table_html}
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)