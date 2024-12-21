import os
import sys
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import TransformedTargetRegressor
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import pickle

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numeric_features = ["reading score", "writing score"]
            categorical_features = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course",
            ]

            numeric_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore"))
                ]
            )

            logging.info("Created pipelines for numerical and categorical features.")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numeric_pipeline, numeric_features),
                    ("cat", categorical_pipeline, categorical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Train and test data read successfully.")

            target_column = "math score"

            if target_column not in train_df.columns:
                raise ValueError(f"Target column '{target_column}' missing in train dataset.")
            if target_column not in test_df.columns:
                raise ValueError(f"Target column '{target_column}' missing in test dataset.")

            # Separate input features and target column for both datasets
            input_features_train_df = train_df.drop(columns=[target_column], axis=1)
            target_train_df = train_df[target_column]
            input_features_test_df = test_df.drop(columns=[target_column], axis=1)
            target_test_df = test_df[target_column]
            logging.info("Feature and target columns separated.")

            preprocessor = self.get_data_transformer_object()

            input_features_train_arr = preprocessor.fit_transform(input_features_train_df)
            input_features_test_arr = preprocessor.transform(input_features_test_df)
            logging.info("Preprocessing applied to train and test data.")

            train_array = np.c_[input_features_train_arr, np.array(target_train_df)]
            test_array = np.c_[input_features_test_arr, np.array(target_test_df)]

            save_object(self.data_transformation_config.preprocessor_obj_file_path, preprocessor)

            return train_array, test_array, self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)
