import os
import pandas as pd
import streamlit as st

# Set the Kaggle dataset and temporary directory
DATASET_ID = "jacksoncrow/stock-market-dataset"
TEMP_DIR = "kaggle_temp"

# Ensure the temporary directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

def fetch_kaggle_data(file_name):
    """
    Fetches a specific file from a Kaggle dataset and loads it as a DataFrame.
    
    Args:
        file_name (str): The name of the file to download from the Kaggle dataset.
    
    Returns:
        DataFrame: The requested data as a Pandas DataFrame.
    """
    # Download the file using Kaggle API
    file_path = os.path.join(TEMP_DIR, file_name)
    os.system(f"kaggle datasets download -d {DATASET_ID} -f {file_name} -p {TEMP_DIR} --force")
    
    # Extract the CSV file and load it
    return pd.read_csv(file_path)
