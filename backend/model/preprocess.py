import pandas as pd
import os

# Get the absolute path to the 'data' directory dynamically based on the script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory where this script is located
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')         # Navigate to the data directory from the current location

# File paths (absolute paths)
FINAL_DATA_PATH = os.path.join(DATA_DIR, 'FINALDATA.csv')
PROCESSED_FINAL_DATA_PATH = os.path.join(DATA_DIR, 'processed_FINALDATA.csv')

# Function to preprocess FINALDATA.csv
def preprocess_final_data(filepath):
    # Read the raw FINALDATA.csv
    df = pd.read_csv(filepath)
    
    # Standardize column names by stripping any extra spaces
    df.columns = df.columns.str.strip()
    
    # Ensure the required columns exist
    if "MIC Value" not in df.columns:
        raise KeyError("The column 'MIC Value' is missing from FINALDATA.csv. Please check the file.")
    if "Interpretation" not in df.columns:
        raise KeyError("The column 'Interpretation' is missing from FINALDATA.csv. Please check the file.")
    
    # Process the 'MIC Value' column: remove any extraneous characters and convert to a float
    def clean_mic_value(x):
        if isinstance(x, str):
            try:
                # Remove any leading characters such as <, >, or =, then convert to float
                return float(x.lstrip("<>=").strip().split()[0])
            except ValueError:
                print(f"Warning: Could not convert MIC Value '{x}' to float. Setting it to NaN.")
                return None
        return x  # If numeric, leave it as is

    df["MIC Value"] = df["MIC Value"].apply(clean_mic_value)
    df = df.dropna(subset=["MIC Value"])  # Drop any rows where MIC Value could not be converted
    
    # Save the processed data to a new file for use by the API
    df.to_csv(PROCESSED_FINAL_DATA_PATH, index=False)
    print(f"Processed FINALDATA.csv saved to {PROCESSED_FINAL_DATA_PATH}")

# Run the preprocessing function when the script is executed directly
if __name__ == "__main__":
    preprocess_final_data(FINAL_DATA_PATH)
