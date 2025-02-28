# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# import pickle
# import os
# from model.preprocess import preprocess_mic  # Import preprocess_mic function

# app = Flask(__name__)
# CORS(app)

# # Get the absolute path to the 'data' and 'model' directories dynamically
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory where this script is located
# DATA_DIR = os.path.join(BASE_DIR, 'data')  # Correct path for data directory inside 'backend'
# MODEL_DIR = os.path.join(BASE_DIR, '..', 'model')  # Navigate to the model directory

# # Ensure the model directory exists
# os.makedirs(MODEL_DIR, exist_ok=True)

# # Load trained model using pickle
# with open(os.path.join(MODEL_DIR, 'trained_model.pkl'), 'rb') as model_file:
#     model = pickle.load(model_file)

# # Load feature names saved during model training
# with open(os.path.join(MODEL_DIR, 'feature_names.pkl'), 'rb') as f:
#     saved_feature_names = pickle.load(f)

# mic_data = pd.read_csv(os.path.join(DATA_DIR, 'standard_mic.csv'))
# mic_data.columns = mic_data.columns.str.strip().str.upper()  # Normalize column names

# # Load bacteria and antibiotics options from the dataset
# df = pd.read_csv(os.path.join(DATA_DIR, 'processed_FINALDATA.csv'))  # Make sure to use the processed data

# # Ensure column names are stripped of any leading/trailing spaces
# df.columns = df.columns.str.strip()

# # Load bacteria and antibiotic options
# bacteria_list = df['Name of the Bacteria'].unique().tolist()  
# antibiotics_list = df['Antibiotic Prescribed'].unique().tolist()  

# # Map user exposure levels to MIC Interpretation
# exposure_mapping = {
#     1: 'S',  # Minimal or No Exposure -> Sensitive
#     2: 'I',  # Moderate Exposure -> Intermediate
#     3: 'R'   # Frequent or Prolonged Exposure -> Resistant
# }

# # Home route
# @app.route('/')
# def home():
#     return "Welcome to the UTI Antibiotic Resistance Prediction API!"

# # Favicon route to avoid 404 error
# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # Return no content for favicon request


# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Get data from request
#         data = request.get_json()

#         # Ensure valid exposure level
#         exposure_level = int(data.get('exposure_level'))
#         if exposure_level not in exposure_mapping:
#             raise ValueError("Invalid exposure level. Must be 1, 2, or 3.")
        
#         # User interpretation based on exposure level
#         user_interpretation = exposure_mapping[exposure_level]
#         print(f"User Interpretation (Exposure Level {exposure_level}): {user_interpretation}")  # Debugging

#         # Extract bacteria and antibiotic from user input
#         bacteria = f"Name of the Bacteria_{data['bacteria'].upper().strip()}"
#         antibiotic = f"Antibiotic Prescribed_{data['antibiotic'].upper().strip()}"

#         # Validate that user-specified bacteria and antibiotic are in the model's features
#         if bacteria not in saved_feature_names or antibiotic not in saved_feature_names:
#             raise ValueError(f"Invalid bacteria or antibiotic feature not found in model's features. Bacteria: {bacteria}, Antibiotic: {antibiotic}")

#         # Create input dataframe for prediction (use a dummy MIC value)
#         input_features = pd.DataFrame({
#             "MIC Value": [0],
#             bacteria: [1],
#             antibiotic: [1]
#         })

#         # Reindex to match the model's expected features
#         input_features = input_features.reindex(columns=saved_feature_names, fill_value=0)

#         # Perform model prediction
#         prediction = model.predict(input_features)
#         print(f"Model Prediction Output: {prediction}")  # Debugging: What is the raw prediction?

#         # Model interpretation based on prediction
#         if prediction[0] == 2:
#             model_interpretation = "Resistant"
#         elif prediction[0] == 1:
#             model_interpretation = "Sensitive"
#         else:
#             model_interpretation = "Sensitive"
        
#         print(f"Model Interpretation: {model_interpretation}")  # Debugging: What is the mapped model interpretation?

#         # Adjust model interpretation based on user exposure level
#         if user_interpretation == "R":  
#             model_interpretation = "Resistant"
#         elif user_interpretation == "I":  
#             model_interpretation = "Sensitive"
#         elif user_interpretation == "S":  
#             model_interpretation = "Sensitive"

#         print(f"Adjusted Model Interpretation (based on exposure level): {model_interpretation}")  # Debugging

#         # Now, query FINALDATA.csv for the interpretation based on bacteria and antibiotic
#         selected_bacteria = data['bacteria'].strip().upper()
#         selected_antibiotic = data['antibiotic'].strip().upper()

#         # Find the corresponding row in the FINALDATA dataframe for the model interpretation
#         model_data_row = df[
#             (df['Name of the Bacteria'].str.upper() == selected_bacteria) & 
#             (df['Antibiotic Prescribed'].str.upper() == selected_antibiotic)
#         ]
        
#         if model_data_row.empty:
#             raise ValueError(f"No matching data found for Bacteria: {selected_bacteria} and Antibiotic: {selected_antibiotic} in model training data.")

#         # Extract the MIC value from FINALDATA.csv based on the model interpretation
#         model_mic_value = model_data_row.loc[model_data_row['Interpretation'] == model_interpretation, 'MIC Value'].values

#         # If no MIC value is found for the interpretation, return "Unknown"
#         mic_value = model_mic_value[0] if model_mic_value.size > 0 else "Unknown"

#         # Return both user and model interpretations
#         return jsonify({
#             "user_interpretation": user_interpretation,
#             "model_interpretation": model_interpretation,
#             "mic_value": mic_value
#         })

#     except Exception as e:
#         print(f"Error during prediction: {str(e)}")
#         return jsonify({"error": f"Error during prediction: {str(e)}"}), 400


# @app.route('/get-options', methods=['GET'])
# def get_options():
#     try:
#         # Extract bacteria and antibiotics options from the dataframe
#         bacteria = [name.strip() for name in bacteria_list]  # Strip any leading/trailing spaces
#         antibiotics = [name.strip().upper() for name in antibiotics_list]  # Convert to uppercase
#         return jsonify({
#             "bacteria": bacteria,
#             "antibiotics": antibiotics
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Dynamically set the path to the data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Load the dataset that contains:
# [Name of the Bacteria, Antibiotic Prescribed, MIC Value, Interpretation]
df = pd.read_csv(os.path.join(DATA_DIR, 'processed_FINALDATA.csv'))
df.columns = df.columns.str.strip()  # Clean up any extra spaces in column names

# Pre-extract lists for bacteria and antibiotics (unfiltered)
bacteria_list = df['Name of the Bacteria'].unique().tolist()
antibiotics_list = df['Antibiotic Prescribed'].unique().tolist()

# Mapping for the exposure level options:
# 1 -> Sensitive (S), 2 -> Resistant (R)
interpretation_mapping = {
    1: 'S',
    2: 'R'
}

@app.route('/')
def home():
    return "Welcome to the UTI Antibiotic Resistance Prediction API!"

# Favicon route to avoid 404 errors
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Prediction endpoint: Returns the MIC value based on bacteria, antibiotic, and the selected exposure option.
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the request
        data = request.get_json()

        # Validate and map the exposure level to an interpretation letter
        exposure_level = int(data.get('exposure_level'))
        if exposure_level not in interpretation_mapping:
            raise ValueError("Invalid exposure level. Must be 1 or 2.")
        selected_interpretation = interpretation_mapping[exposure_level]

        # Extract bacteria and antibiotic from the request
        bacteria = data.get('bacteria')
        antibiotic = data.get('antibiotic')
        if not bacteria or not antibiotic:
            raise ValueError("Both bacteria and antibiotic must be provided.")

        # Standardize input (uppercase and strip extra spaces)
        selected_bacteria = bacteria.strip().upper()
        selected_antibiotic = antibiotic.strip().upper()

        # Filter the dataset for matching bacteria and antibiotic
        filtered_df = df[
            (df['Name of the Bacteria'].str.upper() == selected_bacteria) &
            (df['Antibiotic Prescribed'].str.upper() == selected_antibiotic)
        ]
        if filtered_df.empty:
            raise ValueError(f"No matching data found for Bacteria: {selected_bacteria} and Antibiotic: {selected_antibiotic}.")

        # Filter further based on the interpretation (S, I, or R)
        result_row = filtered_df[filtered_df['Interpretation'] == selected_interpretation]
        if result_row.empty:
            mic_value = "Unknown"
        else:
            mic_value = result_row.iloc[0]['MIC Value']

        return jsonify({
            "interpretation": selected_interpretation,
            "mic_value": mic_value
        })

    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 400

# Get options endpoint: Optionally filters antibiotics based on a selected bacteria.
@app.route('/get-options', methods=['GET'])
def get_options():
    try:
        # If a bacteria query parameter is provided, filter antibiotics for that bacteria.
        bacteria_param = request.args.get('bacteria', None)
        if bacteria_param:
            filtered_df = df[df['Name of the Bacteria'].str.upper() == bacteria_param.strip().upper()]
            antibiotics = filtered_df['Antibiotic Prescribed'].unique().tolist()
        else:
            antibiotics = antibiotics_list

        return jsonify({
            "bacteria": [b.strip() for b in bacteria_list],
            "antibiotics": [a.strip().upper() for a in antibiotics]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/get-options', methods=['GET'])
# def get_options():
#     try:
#         bacteria_param = request.args.get('bacteria', None)
#         exposure_level = request.args.get('exposure_level', None)

#         if not bacteria_param or not exposure_level:
#             return jsonify({"error": "Bacteria and exposure level are required."}), 400

#         # Map exposure level to interpretation ('S' or 'R')
#         exposure_level = int(exposure_level)
#         if exposure_level not in interpretation_mapping:
#             return jsonify({"error": "Invalid exposure level. Must be 1 or 2."}), 400

#         interpretation = interpretation_mapping[exposure_level]

#         # Filter dataset based on bacteria and interpretation
#         filtered_df = df[
#             (df['Name of the Bacteria'].str.upper() == bacteria_param.strip().upper()) &
#             (df['Interpretation'] == interpretation)
#         ]

#         antibiotics = filtered_df['Antibiotic Prescribed'].unique().tolist()

#         return jsonify({
#             "bacteria": [b.strip() for b in bacteria_list],
#             "antibiotics": [a.strip().upper() for a in antibiotics]
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

