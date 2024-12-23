# Purely created for Deployment in aws Beanstalk as 
# As in the AWS documantation application:application is written
from flask import Flask, request, jsonify, render_template
from src.pipeline.predict_pipeline import PredictPipeline, CustomData
from src.exception import CustomException
import numpy as np 
import pandas as pd 

from sklearn.preprocessing import StandardScaler


# IN terminal write python app.py 
# Then go to your Defalult Browser and type 127.0.0.1:5000 (5000 is the Default port)
application = Flask(__name__)
app = application 

# Route for Home Page 
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Home route for displaying the input form and making predictions.
    """
    if request.method == "POST":
        try:
            # Collect form data
            gender = request.form.get("gender")
            race_ethnicity = request.form.get("race_ethnicity")
            parental_level_of_education = request.form.get("parental_level_of_education")
            lunch = request.form.get("lunch")
            test_preparation_course = request.form.get("test_preparation_course")
            reading_score = float(request.form.get("reading_score"))
            writing_score = float(request.form.get("writing_score"))

            # Create CustomData object
            input_data = CustomData(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=reading_score,
                writing_score=writing_score,
            )

            # Convert to DataFrame
            input_df = input_data.get_data_as_dataframe()

            # Use PredictPipeline for predictions
            predict_pipeline = PredictPipeline()
            prediction = predict_pipeline.predict(input_df)

            return render_template(
                "index.html",
                prediction_text=f"Predicted Math Score: {prediction[0]}",
            )
        except Exception as e:
            return render_template(
                "index.html",
                prediction_text=f"An error occurred: {str(e)}",
            )

    # Default behavior for GET request
    return render_template("index.html")


@app.route("/predict_data", methods=["POST"])
def predict_data():
    if request=='GET':
        return render_template("home.html")
    else:    
        """
        API route for making predictions via JSON data.
        """
        try:
            # Parse JSON input
            data = request.json
            custom_data = CustomData(
                gender=data["gender"],
                race_ethnicity=data["race_ethnicity"],
                parental_level_of_education=data["parental_level_of_education"],
                lunch=data["lunch"],
                test_preparation_course=data["test_preparation_course"],
                reading_score=float(data["reading_score"]),
                writing_score=float(data["writing_score"]),
            )

            # Convert to DataFrame
            input_df = custom_data.get_data_as_dataframe()
            print(input_df)

            # Make prediction
            predict_pipeline = PredictPipeline()
            prediction = predict_pipeline.predict(input_df)

            return render_template('home.html',prediction=prediction[0])
        except Exception as e:
            return jsonify({"error": str(e)}), 400

# Removed debug = True for deployment it is nor needed
if __name__ == "__main__":
    app.run(host = '0.0.0.0') 
