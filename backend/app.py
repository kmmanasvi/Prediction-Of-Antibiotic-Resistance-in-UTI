from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from model.preprocess import preprocess_mic  # Import preprocess_mic function

app = Flask(__name__)
CORS(app)

# Load trained model using pickle
with open('model/trained_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load feature names saved during model training
with open('model/feature_names.pkl', 'rb') as f:
    saved_feature_names = pickle.load(f)

# Load bacteria and antibiotics options from the dataset
df = pd.read_csv('data/FINALDATA.csv')

# Ensure column names are stripped of any leading/trailing spaces
df.columns = df.columns.str.strip()

# Load bacteria and antibiotic options
bacteria_list = df['Name of the Bacteria'].unique().tolist()  
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
        # Get data from the request
        data = request.get_json()

        # Preprocess MIC value
        mic_value = preprocess_mic(data['mic_value'])

        if mic_value is None:
            raise ValueError("Invalid MIC value format.")

        # Format bacteria and antibiotic columns
        bacteria = f"Name of the Bacteria_{data['bacteria'].upper().strip()}"
        antibiotic = f"Antibiotic Prescribed_{data['antibiotic'].upper().strip()}"

        # Ensure bacteria and antibiotic are in saved feature names
        if bacteria not in saved_feature_names:
            raise ValueError(f"Bacteria feature '{bacteria}' not found in the model's feature names.")
        if antibiotic not in saved_feature_names:
            raise ValueError(f"Antibiotic feature '{antibiotic}' not found in the model's feature names.")

        # Create the input dataframe for the primary prediction
        input_features = pd.DataFrame({
            "MIC Value": [mic_value],
            bacteria: [1],  # One-hot encoding for bacteria
            antibiotic: [1]  # One-hot encoding for antibiotic
        })

        # Reindex to match saved features, ensuring missing columns are set to 0
        input_features = input_features.reindex(columns=saved_feature_names, fill_value=0)

        # Make the primary prediction using the model
        prediction = model.predict(input_features)
        interpretation = "Resistant" if int(prediction[0]) == 1 else "Sensitive"

        # Filter dataset for antibiotics associated with the selected bacteria
        filtered_antibiotics = df[df['Name of the Bacteria'].str.strip().str.upper() == data['bacteria'].upper().strip()]['Antibiotic Prescribed'].unique()

        # Predict interpretations for other antibiotics
        other_interpretations = {}
        for ab in filtered_antibiotics:
            ab_feature = f"Antibiotic Prescribed_{ab.upper().strip()}"

            # Reset input features and set bacteria/antibiotic features for current antibiotic
            temp_input_features = pd.DataFrame({
                "MIC Value": [mic_value],
                bacteria: [1],  # Bacteria feature remains active
            })
            temp_input_features = temp_input_features.reindex(columns=saved_feature_names, fill_value=0)
            
            if ab_feature in saved_feature_names:
                temp_input_features[ab_feature] = 1  # Set the current antibiotic feature to 1
                other_prediction = model.predict(temp_input_features)
                other_interpretations[ab] = "Resistant" if int(other_prediction[0]) == 1 else "Sensitive"

        return jsonify({
            "interpretation": interpretation,
            "other_interpretations": other_interpretations
        })

    except Exception as e:
        print("Error:", str(e))  # Print error for debugging
        return jsonify({"error": str(e)}), 400


@app.route('/get-options', methods=['GET'])
def get_options():
    try:
        # Extract bacteria and antibiotics options from the dataframe
        bacteria = [name.strip() for name in bacteria_list]  # Strip any leading/trailing spaces
        antibiotics = [name.strip().upper() for name in antibiotics_list]  # Convert to uppercase
        return jsonify({
            "bacteria": bacteria,
            "antibiotics": antibiotics
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/debug-features', methods=['GET'])
def debug_features():
    try:
        # Convert the pandas Index to a list before returning
        feature_names_list = saved_feature_names.tolist()
        return jsonify({"feature_names": feature_names_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
