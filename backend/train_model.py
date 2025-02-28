import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os

# Get the absolute path to the 'data' and 'model' directories dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory where this script is located
DATA_DIR = os.path.join(BASE_DIR, 'data')  # Navigate to the correct data directory (backend/data)
MODEL_DIR = os.path.join(BASE_DIR, '..', 'model')  # Navigate to the model directory

# Ensure the model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load the dataset 
df = pd.read_csv(os.path.join(DATA_DIR, 'processed_FINALDATA.csv'))  # Make sure to use the processed data

# Function to clean and convert MIC values
def preprocess_mic(value):
    """
    Convert MIC values to numerical equivalents.
    Handles ranges like <=16 or >=4 by using the numerical part only.
    """
    if isinstance(value, str):
        value = value.replace('<=', '').replace('>=', '').replace('<', '').replace('>', '').strip()
    try:
        return float(value)
    except ValueError:
        return np.nan

# Apply MIC preprocessing
df['MIC Value'] = df['MIC Value'].apply(preprocess_mic)

# Map Interpretation to numerical values
df['Interpretation'] = df['Interpretation'].map({'S': 0, 'R': 1})

# One-hot encode categorical variables
df.columns = df.columns.str.strip()  # Remove trailing spaces in column names
df_encoded = pd.get_dummies(df, columns=['Name of the Bacteria', 'Antibiotic Prescribed'], drop_first=True)

# Save the feature names for use during prediction
feature_names = df_encoded.drop('Interpretation', axis=1).columns
# print("Feature Names Used During Training:", list(feature_names))  # DEBUG

# Save feature names to a pickle file for later use in prediction
with open(os.path.join(MODEL_DIR, 'feature_names.pkl'), 'wb') as file:
    pickle.dump(feature_names, file)

# Define features and target
X = df_encoded.drop('Interpretation', axis=1)
y = df_encoded['Interpretation']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the trained model
with open(os.path.join(MODEL_DIR, 'trained_model.pkl'), 'wb') as file:
    pickle.dump(rf_model, file)

print("Model and feature names saved successfully!")
