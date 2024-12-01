# model/preprocess.py

def preprocess_mic(value):
    """
    Convert MIC values to numerical equivalents.
    Handles ranges like <=16 or >=4 by using the numerical part only.
    """
    if isinstance(value, str):
        value = value.replace('<=', '').replace('>=', '').replace('=>', '').replace('<', '').replace('>', '').strip()
    try:
        return float(value)
    except ValueError:
        return None  # Return None if the value cannot be converted to a float
