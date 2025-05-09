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
# @app.route('/get-options', methods=['GET'])
# def get_options():
#     try:
#         # If a bacteria query parameter is provided, filter antibiotics for that bacteria.
#         bacteria_param = request.args.get('bacteria', None)
#         if bacteria_param:
#             filtered_df = df[df['Name of the Bacteria'].str.upper() == bacteria_param.strip().upper()]
#             antibiotics = filtered_df['Antibiotic Prescribed'].unique().tolist()
#         else:
#             antibiotics = antibiotics_list

#         return jsonify({
#             "bacteria": [b.strip() for b in bacteria_list],
#             "antibiotics": [a.strip().upper() for a in antibiotics]
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@app.route('/get-options', methods=['GET'])
def get_options():
    try:
        bacteria_param = request.args.get('bacteria', None)
        if bacteria_param:
            print(f"Received bacteria in request: {bacteria_param}")  # Debugging
            # filtered_df = df[df['Name of the Bacteria'].str.upper().str.strip() == bacteria_param.strip().upper()]
            filtered_df = df[df['Name of the Bacteria'].str.upper().str.strip().str.contains(bacteria_param, regex=False)]
            print(f"Filtered antibiotics: {filtered_df['Antibiotic Prescribed'].unique()}")  # Debugging
            antibiotics = filtered_df['Antibiotic Prescribed'].unique().tolist()
        else:
            antibiotics = antibiotics_list

        return jsonify({
            "bacteria": [b.strip() for b in bacteria_list],
            "antibiotics": [a.strip().upper() for a in antibiotics]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_antibiotics', methods=['GET'])
def get_antibiotics():
    """Fetch antibiotics based on selected bacteria and exposure level."""
    try:
        # Get query parameters
        bacteria = request.args.get('bacteria', None)
        exposure_level = request.args.get('exposure_level', type=int)

        # Ensure parameters are provided
        if not bacteria or exposure_level not in interpretation_mapping:
            return jsonify({"error": "Both bacteria and a valid exposure level (1 or 2) are required."}), 400

        # Map exposure level to 'S' or 'R'
        level = interpretation_mapping[exposure_level]

        # Standardize input (uppercase and strip spaces)
        selected_bacteria = bacteria.strip().upper()

        # Filter antibiotics based on bacteria and interpretation (S or R)
        filtered_df = df[
            (df['Name of the Bacteria'].str.upper() == selected_bacteria) &
            (df['Interpretation'] == level)
        ]

        # Extract unique antibiotics
        antibiotics = filtered_df['Antibiotic Prescribed'].dropna().unique().tolist()

        return jsonify({"antibiotics": sorted(antibiotics)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

