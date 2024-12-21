import os
import sys
from src.logger import logging

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}
        fitted_models = {}  # Store fitted models

        for model_name, model in models.items():
            logging.info(f"Training {model_name}")
            para = param[model_name]

            if len(para) == 0:  # For models without hyperparameters like Linear Regression
                model.fit(X_train, y_train)
                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)
                fitted_models[model_name] = model
            else:
                gs = GridSearchCV(
                    estimator=model,
                    param_grid=para,
                    cv=3,
                    n_jobs=-1,
                    verbose=2
                )
                gs.fit(X_train, y_train)
                
                model = gs.best_estimator_
                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)
                fitted_models[model_name] = model

            test_model_score = r2_score(y_test, y_test_pred)
            train_model_score = r2_score(y_train, y_train_pred)
            
            logging.info(f"{model_name} Train Score: {train_model_score}")
            logging.info(f"{model_name} Test Score: {test_model_score}")
            
            report[model_name] = test_model_score

        return report, fitted_models

    except Exception as e:
        logging.error(f"Error in evaluate_models: {str(e)}")
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)