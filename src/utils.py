import os
import sys
import dill
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"Object saved at {file_path}")
    except Exception as e:
        raise CustomException(e, sys)


# # Load an object (e.g., preprocessor, model) from a file
# def load_object(file_path):
#     """
#     Loads an object from a specified file path using dill.
    
#     :param file_path: Path where the object is saved.
#     :return: Loaded object.
#     """
#     try:
#         with open(file_path, "rb") as file_obj:
#             logging.info(f"Object loaded from {file_path}")
#             return dill.load(file_obj)
#     except Exception as e:
#         raise CustomException(e, sys)

# # Save a NumPy array to a CSV file
# def save_numpy_array(file_path, array):
#     """
#     Saves a NumPy array to a specified CSV file.
    
#     :param file_path: Path where the NumPy array will be saved.
#     :param array: NumPy array to save.
#     """
#     try:
#         dir_path = os.path.dirname(file_path)
#         os.makedirs(dir_path, exist_ok=True)
#         np.savetxt(file_path, array, delimiter=",")
#         logging.info(f"NumPy array saved at {file_path}")
#     except Exception as e:
#         raise CustomException(e, sys)

# # Load a NumPy array from a CSV file
# def load_numpy_array(file_path):
#     """
#     Loads a NumPy array from a specified CSV file.
    
#     :param file_path: Path where the NumPy array is saved.
#     :return: Loaded NumPy array.
#     """
#     try:
#         logging.info(f"NumPy array loaded from {file_path}")
#         return np.loadtxt(file_path, delimiter=",")
#     except Exception as e:
#         raise CustomException(e, sys)
