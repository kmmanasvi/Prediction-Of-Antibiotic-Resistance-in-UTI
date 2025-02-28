# import pandas as pd
# import os


# # Get the absolute path to the 'data' directory dynamically based on the script's location
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory where this script is located
# DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # Navigate to the data directory from the backend folder

# # File paths (now absolute paths)
# FINAL_DATA_PATH = os.path.join(DATA_DIR, 'FINALDATA.csv')
# STANDARD_MIC_PATH = os.path.join(DATA_DIR, 'standard_mic.csv')
# PROCESSED_FINAL_DATA_PATH = os.path.join(DATA_DIR, 'processed_FINALDATA.csv')
# PROCESSED_STANDARD_MIC_PATH = os.path.join(DATA_DIR, 'processed_StandardMIC.csv')
# PROCESSED_MIC_PATH = os.path.join(DATA_DIR, 'processed_MIC.csv')

# # Function to preprocess FINALDATA.csv
# def preprocess_final_data(filepath):
#     # Read the data
#     df = pd.read_csv(filepath)
    
#     # Rename columns to standardize them (strip any extra spaces)
#     df.columns = df.columns.str.strip()
    
#     # Ensure correct column names
#     if "MIC Value" not in df.columns:
#         raise KeyError("The column 'MIC Value' is missing from FINALDATA.csv. Please check the file.")

#     # Process the 'MIC Value' column
#     def clean_mic_value(x):
#         if isinstance(x, str):
#             # Remove non-numeric characters (like "<=" or ">=") and convert to float
#             try:
#                 return float(x.lstrip("<>=").strip().split()[0])
#             except ValueError:
#                 print(f"Warning: Could not convert MIC Value '{x}' to float. Setting it to NaN.")
#                 return None
#         return x  # Leave numeric values as is

#     df["MIC Value"] = df["MIC Value"].apply(clean_mic_value)
    
#     # Save the processed data
#     df.to_csv(PROCESSED_FINAL_DATA_PATH, index=False)
#     print(f"Processed FINALDATA.csv saved to {PROCESSED_FINAL_DATA_PATH}")

# # Function to preprocess standard_mic.csv
# def preprocess_standard_mic(filepath):
#     """
#     Process the Standard MIC data to clean and standardize it.
#     """
#     # Load the data
#     df = pd.read_csv(filepath)

#     # Rename columns to standardize them
#     df.columns = ["Name of the Bacteria", "Antibiotic Prescribed", "Resistance (R)", "Intermediate (I)", "Sensitive (S)"]

#     # Strip extra spaces and reorder columns for consistency
#     df["Resistance (R)"] = df["Resistance (R)"].str.strip()
#     df["Intermediate (I)"] = df["Intermediate (I)"].str.strip()
#     df["Sensitive (S)"] = df["Sensitive (S)"].str.strip()

#     # Reorder columns to maintain logical flow
#     df = df[["Name of the Bacteria", "Antibiotic Prescribed", "Sensitive (S)", "Intermediate (I)", "Resistance (R)"]]

#     # Save processed data
#     df.to_csv(PROCESSED_STANDARD_MIC_PATH, index=False)
#     print(f"Processed standard_mic.csv saved to {PROCESSED_STANDARD_MIC_PATH}")

# # Function to preprocess the MIC data (added function)
# def preprocess_mic(filepath):
#     """
#     Function to preprocess MIC data.
#     This function will process the columns 'Sensitive (S)', 'Intermediate (I)', 'Resistance (R)' from the input file.
#     """
#     # Load the data
#     df = pd.read_csv(filepath)

#     # Ensure the column names are clean and standardized
#     df.columns = df.columns.str.strip()

#     # Process the columns 'Sensitive (S)', 'Intermediate (I)', 'Resistance (R)'
#     df['Sensitive (S)'] = df['Sensitive (S)'].apply(lambda x: 1 if x == 'S' else 0)
#     df['Intermediate (I)'] = df['Intermediate (I)'].apply(lambda x: 1 if x == 'I' else 0)
#     df['Resistance (R)'] = df['Resistance (R)'].apply(lambda x: 1 if x == 'R' else 0)

#     # Save the processed data to a new file
#     df.to_csv(PROCESSED_MIC_PATH, index=False)
#     print(f"Processed MIC data saved to {PROCESSED_MIC_PATH}")

# # Run the preprocessing functions
# if __name__ == "__main__":
#     preprocess_final_data(FINAL_DATA_PATH)
#     preprocess_standard_mic(STANDARD_MIC_PATH)
#     preprocess_mic(STANDARD_MIC_PATH) 



# import pandas as pd
# import os

# # Get the absolute path to the 'data' directory dynamically based on the script's location
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory where this script is located
# DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # Navigate to the data directory from the backend folder

# # File paths (now absolute paths)
# FINAL_DATA_PATH = os.path.join(DATA_DIR, 'FINALDATA.csv')
# STANDARD_MIC_PATH = os.path.join(DATA_DIR, 'standard_mic.csv')
# PROCESSED_FINAL_DATA_PATH = os.path.join(DATA_DIR, 'processed_FINALDATA.csv')
# PROCESSED_STANDARD_MIC_PATH = os.path.join(DATA_DIR, 'processed_StandardMIC.csv')
# PROCESSED_MIC_PATH = os.path.join(DATA_DIR, 'processed_MIC.csv')

# # Function to preprocess FINALDATA.csv
# def preprocess_final_data(filepath):
#     df = pd.read_csv(filepath)
    
#     # Rename columns to standardize them (strip any extra spaces)
#     df.columns = df.columns.str.strip()
    
#     # Ensure correct column names
#     if "MIC Value" not in df.columns:
#         raise KeyError("The column 'MIC Value' is missing from FINALDATA.csv. Please check the file.")

#     # Process the 'MIC Value' column
#     def clean_mic_value(x):
#         if isinstance(x, str):
#             try:
#                 return float(x.lstrip("<>=").strip().split()[0])
#             except ValueError:
#                 print(f"Warning: Could not convert MIC Value '{x}' to float. Setting it to NaN.")
#                 return None
#         return x  # Leave numeric values as is

#     df["MIC Value"] = df["MIC Value"].apply(clean_mic_value)
#     df = df.dropna(subset=["MIC Value"])  # Drop rows where MIC Value could not be converted

#     # Save the processed data
#     df.to_csv(PROCESSED_FINAL_DATA_PATH, index=False)
#     print(f"Processed FINALDATA.csv saved to {PROCESSED_FINAL_DATA_PATH}")

# # Function to preprocess standard_mic.csv
# def preprocess_standard_mic(filepath):
#     df = pd.read_csv(filepath)

#     # Rename columns to standardize them
#     df.columns = ["Name of the Bacteria", "Antibiotic Prescribed", "Resistance (R)", "Intermediate (I)", "Sensitive (S)"]

#     # Strip extra spaces and reorder columns for consistency
#     df["Resistance (R)"] = df["Resistance (R)"].str.strip()
#     df["Intermediate (I)"] = df["Intermediate (I)"].str.strip()
#     df["Sensitive (S)"] = df["Sensitive (S)"].str.strip()

#     # Reorder columns to maintain logical flow
#     df = df[["Name of the Bacteria", "Antibiotic Prescribed", "Sensitive (S)", "Intermediate (I)", "Resistance (R)"]]

#     # Save processed data
#     df.to_csv(PROCESSED_STANDARD_MIC_PATH, index=False)
#     print(f"Processed standard_mic.csv saved to {PROCESSED_STANDARD_MIC_PATH}")

# # Function to preprocess the MIC data
# def preprocess_mic(filepath):
#     df = pd.read_csv(filepath)

#     # Ensure the column names are clean and standardized
#     df.columns = df.columns.str.strip()

#     # Process the columns 'Sensitive (S)', 'Intermediate (I)', 'Resistance (R)'
#     df['Sensitive (S)'] = df['Sensitive (S)'].apply(lambda x: 1 if x == 'S' else 0 if pd.notnull(x) else None)
#     df['Intermediate (I)'] = df['Intermediate (I)'].apply(lambda x: 1 if x == 'I' else 0 if pd.notnull(x) else None)
#     df['Resistance (R)'] = df['Resistance (R)'].apply(lambda x: 1 if x == 'R' else 0 if pd.notnull(x) else None)

#     # Save the processed data to a new file
#     df.to_csv(PROCESSED_MIC_PATH, index=False)
#     print(f"Processed MIC data saved to {PROCESSED_MIC_PATH}")

# # Run the preprocessing functions
# if __name__ == "__main__":
#     preprocess_final_data(FINAL_DATA_PATH)
#     preprocess_standard_mic(STANDARD_MIC_PATH)
#     preprocess_mic(STANDARD_MIC_PATH)



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
