from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle  
from model.preprocess import preprocess_mic


app = Flask(__name__)
CORS(app)

# Load the trained model using pickle
with open('model/trained_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load bacteria and antibiotics options from the dataset
df = pd.read_excel('data/FINALDATA.xlsx')
bacteria_list = df['Name of the Bacteria '].unique().tolist()
antibiotics_list = df['Antibiotic Prescribed'].unique().tolist()

# Home route
@app.route('/')
def home():
    return "Welcome to the UTI Antibiotic Resistance Prediction API!"

# Favicon route to avoid 404 error
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return no content for favicon request


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        mic_value = preprocess_mic(data['mic_value'])
        bacteria = data['bacteria']
        antibiotic = data['antibiotic']

        # Ensure the feature names match the ones used in training
        features = {f'Name of the Bacteria_{bacteria}': 1, f'Antibiotic Prescribed_{antibiotic}': 1}
        # Make sure we add all other features with 0, even if they aren't selected
        features.update({col: 0 for col in model.feature_names_in_ if col not in features})

        # Don't forget to include the MIC value
        features['MIC Value'] = mic_value

        # Convert features to a DataFrame to match model input
        input_df = pd.DataFrame([features])

        # Make prediction
        prediction = model.predict(input_df)[0]
        other_predictions = {}

        # Predict for other antibiotics
        for other_antibiotic in antibiotics_list:
            if other_antibiotic != antibiotic:
                input_df[f'Antibiotic Prescribed_{other_antibiotic}'] = 1
                input_df[f'Antibiotic Prescribed_{antibiotic}'] = 0
                other_predictions[other_antibiotic] = model.predict(input_df)[0]

        # Return the interpretation and predictions for other antibiotics
        return jsonify({
            'interpretation': 'Sensitive' if prediction == 0 else 'Resistant',
            'other_interpretations': other_predictions or {}  # Empty dictionary if no predictions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400



# Options route
# @app.route('/options', methods=['GET'])
# def get_options():
#     return jsonify({'bacteria': bacteria_list, 'antibiotics': antibiotics_list})

@app.route('/get-options', methods=['GET'])
def get_options():
    try:
        # Extract feature names from the trained model
        feature_names = model.feature_names_in_  # sklearn >= 1.0
        bacteria = [name.split("_")[1] for name in feature_names if name.startswith("Name of the Bacteria _")]
        antibiotics = [name.split("_")[1] for name in feature_names if name.startswith("Antibiotic Prescribed_")]

        return jsonify({
            "bacteria": bacteria,
            "antibiotics": antibiotics
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# import pickle
# from model.preprocess import preprocess_mic

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Restricting CORS to frontend origin

# # Load the trained model using pickle
# with open('model/trained_model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# # Load bacteria and antibiotics options from the dataset
# df = pd.read_excel('data/FINALDATA.xlsx')
# bacteria_list = df['Name of the Bacteria '].unique().tolist()
# antibiotics_list = df['Antibiotic Prescribed'].unique().tolist()

# # Home route
# @app.route('/')
# def home():
#     return "Welcome to the UTI Antibiotic Resistance Prediction API!"

# # Favicon route to avoid 404 error
# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # Return no content for favicon request

# # Prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Receive incoming JSON data
#         data = request.json
#         print(f"Received data: {data}")  # Log incoming data

#         # Extract values
#         mic_value = preprocess_mic(data['mic_value'])
#         bacteria = data['bacteria']
#         antibiotic = data['antibiotic']
#         print(f"Processed MIC: {mic_value}, Bacteria: {bacteria}, Antibiotic: {antibiotic}")  # Log processed values

#         # Prepare input features for model
#         features = {f'Name of the Bacteria _{bacteria}': 1, f'Antibiotic Prescribed_{antibiotic}': 1}
#         features.update({col: 0 for col in model.feature_names_in_ if col not in features})
#         features['MIC Value'] = mic_value

#         # Convert to DataFrame
#         input_df = pd.DataFrame([features])
#         print(f"Input DataFrame for prediction: {input_df}")  # Log input DataFrame

#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         other_predictions = {}

#         # Predict interpretations for other antibiotics
#         for other_antibiotic in antibiotics_list:
#             if other_antibiotic != antibiotic:
#                 input_df[f'Antibiotic Prescribed_{other_antibiotic}'] = 1
#                 input_df[f'Antibiotic Prescribed_{antibiotic}'] = 0
#                 other_predictions[other_antibiotic] = model.predict(input_df)[0]

#         # Return the prediction and other antibiotic interpretations
#         return jsonify({
#             'interpretation': 'Sensitive' if prediction == 0 else 'Resistant',
#             'other_interpretations': other_predictions or {}  # Ensure it's an empty object if no predictions
#         })

#     except KeyError as e:
#         # Return specific error for missing field
#         return jsonify({'error': f"Missing field in input: {str(e)}"}), 400
#     except Exception as e:
#         # General error handler
#         print(f"Error occurred: {e}")  # Log error details
#         return jsonify({'error': str(e)}), 400

# # Options route to get bacteria and antibiotic list
# @app.route('/options', methods=['GET'])
# def get_options():
#     return jsonify({'bacteria': bacteria_list, 'antibiotics': antibiotics_list})

# if __name__ == '__main__':
#     app.run(debug=True)
