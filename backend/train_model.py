# import pandas as pd
# import numpy as np
# import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# # Load the dataset
# df = pd.read_excel('data/FINALDATA.xlsx')

# # Function to clean and convert MIC values
# def preprocess_mic(value):
#     """
#     Convert MIC values to numerical equivalents.
#     Handles ranges like <=16 or >=4 by using the numerical part only.
#     """
#     if isinstance(value, str):
#         value = value.replace('<=', '').replace('>=', '').replace('<', '').replace('>', '').strip()
#     try:
#         return float(value)
#     except ValueError:
#         return np.nan

# df['MIC Value'] = df['MIC Value'].apply(preprocess_mic)

# # Encode "Interpretation" as 0 for 'S' and 1 for 'R'
# df['Interpretation'] = df['Interpretation'].map({'S': 0, 'R': 1})

# # One-hot encode categorical variables
# # df_encoded = pd.get_dummies(df, columns=['Name of the Bacteria ', 'Antibiotic Prescribed'], drop_first=True)
# df.columns = df.columns.str.strip()  # Remove trailing spaces in column names
# df_encoded = pd.get_dummies(df, columns=['Name of the Bacteria', 'Antibiotic Prescribed'], drop_first=True)


# # Define features and target
# X = df_encoded.drop('Interpretation', axis=1)
# y = df_encoded['Interpretation']

# # Split into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the Random Forest model
# rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
# rf_model.fit(X_train, y_train)

# # Evaluate the model
# y_pred = rf_model.predict(X_test)
# print("Confusion Matrix:")
# print(confusion_matrix(y_test, y_pred))
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))
# print("Accuracy:", accuracy_score(y_test, y_pred))

# # Save the model using pickle
# with open('model/trained_model.pkl', 'wb') as file:
#     pickle.dump(rf_model, file)

# print("Model saved successfully!")


import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load the dataset (changed from .xlsx to .csv)
df = pd.read_csv('data/FINALDATA.csv')

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

# Encode "Interpretation" as 0 for 'S' and 1 for 'R'
df['Interpretation'] = df['Interpretation'].map({'S': 0, 'R': 1})

# One-hot encode categorical variables
df.columns = df.columns.str.strip()  # Remove trailing spaces in column names
df_encoded = pd.get_dummies(df, columns=['Name of the Bacteria', 'Antibiotic Prescribed'], drop_first=True)

# Save the feature names for use during prediction
feature_names = df_encoded.drop('Interpretation', axis=1).columns
print("Feature Names Used During Training:", list(feature_names))  # DEBUG

# Save feature names to a pickle file for later use in prediction
with open('model/feature_names.pkl', 'wb') as file:
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
with open('model/trained_model.pkl', 'wb') as file:
    pickle.dump(rf_model, file)

print("Model and feature names saved successfully!")
