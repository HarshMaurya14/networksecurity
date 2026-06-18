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

## Data Transformation related constants
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

##knn imputer to replace missing values in the dataset with the mean of the nearest neighbors. The parameters for the KNN imputer are defined in a dictionary called DATA_TRANSFORMATION_IMPUTER_PARAMS. The missing_values parameter is set to np.nan, which indicates that missing values are represented by NaN (Not a Number) in the dataset. The n_neighbors parameter is set to 3, which means that the imputer will consider the 3 nearest neighbors when calculating the mean to replace missing values. The weights parameter is set to "uniform", which means that all neighbors will be given equal weight when calculating the mean.

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
    "missing_values": np.man,
    "n_neighbours": 3,
    "weights": "uniform",

}
