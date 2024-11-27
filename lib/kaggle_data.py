import os
import pandas as pd
import zipfile
import streamlit as st
import kagglehub


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
KAGGLE_CONFIG_DIR = os.path.join(PROJECT_DIR, "../config")
# Set the Kaggle dataset and temporary directory
TEMP_DIR = os.path.join(PROJECT_DIR, "../kaggle_temp")
DATASET_ID = "jacksoncrow/stock-market-dataset"

# Ensure directories exist
os.environ["KAGGLE_CONFIG_DIR"] = KAGGLE_CONFIG_DIR
os.makedirs(KAGGLE_CONFIG_DIR, exist_ok=True)


def download_dataset(dataset_name, temp_dir=TEMP_DIR):
    """
    Download dataset from Kaggle
    
    Args:
        dataset_name (str): Format should be 'username/dataset-name'
        temp_dir (str): Directory to store downloaded files
    """
    # Create temp directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        path = kagglehub.dataset_download(dataset_name)
        return True
    except Exception as e:
        st.error(f"Error downloading dataset: {str(e)}")
        return False

def get_available_files():
    """
    Lists all CSV files in the downloaded dataset directory
    
    Returns:
        list: List of CSV filenames
    """
    path = kagglehub.dataset_path(DATASET_ID)
    stock_files_path = os.path.join(path, 'stocks')
    if os.path.exists(stock_files_path):
        return [f for f in os.listdir(stock_files_path) if f.endswith('.csv')]
    return []

def fetch_kaggle_data():
    """
    Fetches and extracts the Kaggle dataset zip file.
    
    Returns:
        dict: Paths to the meta file, stocks directory, and ETFs directory.
    """
    zip_path = os.path.join(TEMP_DIR, f"{DATASET_ID.split('/')[-1]}.zip")  # Zip file name
    extraction_marker = os.path.join(TEMP_DIR, "extracted_marker.txt")  # Marker file

    # Check if the zip file already exists locally
    if os.path.exists(zip_path):
        st.info("Dataset already downloaded. Skipping download step.")
    else:
        # Download the dataset
        download_command = f"kaggle datasets download -d {DATASET_ID} -p {TEMP_DIR} --force"
        result = os.system(download_command)
        if result != 0:
            st.error("Failed to download data from Kaggle. Please check your Kaggle API configuration.")
            return {}

    # Check if extraction is needed
    if os.path.exists(extraction_marker):
        st.info("Files already extracted. Skipping extraction step.")
    else:
        # Extract the zip file
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(TEMP_DIR)

            # Create marker file to indicate successful extraction
            with open(extraction_marker, "w") as marker:
                marker.write("Extraction complete")
            
            st.success("Dataset extracted successfully.")
        except Exception as e:
            st.error(f"Failed to extract files from zip: {e}")
            return {}