import os
import sys
import numpy as np
import pandas as pd

TARGET_COLUMN = "Result"

PIPELINE_NAME = "networksecurity"
ARTIFACT_DIR = "artifact"

FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"

DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DATABASE_NAME = "KrishAI"

DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2

## Data Validation related constants

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

## Data Transformation related constants
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

##knn imputer to replace missing values in the dataset with the mean of the nearest neighbors. The parameters for the KNN imputer are defined in a dictionary called DATA_TRANSFORMATION_IMPUTER_PARAMS. The missing_values parameter is set to np.nan, which indicates that missing values are represented by NaN (Not a Number) in the dataset. The n_neighbors parameter is set to 3, which means that the imputer will consider the 3 nearest neighbors when calculating the mean to replace missing values. The weights parameter is set to "uniform", which means that all neighbors will be given equal weight when calculating the mean.

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",

}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"


"""
Model Trainer ralated constant start with MODE TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05

TRAINING_BUCKET_NAME = "netwworksecurity"
