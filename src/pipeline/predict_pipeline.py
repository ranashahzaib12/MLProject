import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass 

    def predict(self, data: pd.DataFrame):        
        """
        Make predictions on the input data.
        Args:
            data (pd.DataFrame): Input data as a Pandas DataFrame.
        Returns:
            list: List of predictions.
        """
        try:
            model_path = 'artifacts\model.pkl'
            preprocessor_path = 'artifacts\preprocessor.pkl'
            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            # Preprocess the input data
            data_scaled= preprocessor.transform(data)

            # Make predictions
            predict = model.predict(data_scaled)

            return predict.tolist()
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: float,
        writing_score: float
    ):
        """
        CustomData class for handling input features for prediction.
        """
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):
        """ 
        Convert the input data into a Pandas DataFrame.
        Returns:
            pd.DataFrame: Input data as a Pandas DataFrame.
        """
        try:
            data = {
                "gender": [self.gender],
                "race/ethnicity": [self.race_ethnicity],
                "parental level of education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test preparation course": [self.test_preparation_course],
                "reading score": [self.reading_score],
                "writing score": [self.writing_score]
            }
            return pd.DataFrame(data)
        except Exception as e:
            raise CustomException(e, sys)

