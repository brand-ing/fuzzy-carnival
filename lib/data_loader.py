import os
import pandas as pd
import streamlit as st

from lib.kaggle_data import TEMP_DIR

def render_data_selector_kaggle():
    """
    Renders the dataset selector for the app.
    Allows users to choose between metadata, stocks, and ETFs.

    Returns:
        DataFrame: Selected and filtered data.
    """
    st.sidebar.title("Dataset Selector")

    # Paths for categorized data
    meta_file = os.path.join(TEMP_DIR, "symbols_valid_meta.csv")
    stocks_dir = os.path.join(TEMP_DIR, "stocks")
    etfs_dir = os.path.join(TEMP_DIR, "etfs")

    # Verify that the required files and directories exist
    data_available = {
        "Meta": os.path.exists(meta_file),
        "Stocks": os.path.exists(stocks_dir) and any(os.listdir(stocks_dir)),
        "ETFs": os.path.exists(etfs_dir) and any(os.listdir(etfs_dir)),
    }

    # Initialize session state for radio button selection
    if "data_type" not in st.session_state:
        st.session_state["data_type"] = "Stocks"  # Default selection

    # Dynamic selection of available data types
    available_data_types = [key for key, available in data_available.items() if available]
    if not available_data_types:
        st.warning("No data available. Please ensure the dataset is downloaded and extracted.")
        return None

    # Persist the radio button selection
    selected_data_type = st.sidebar.radio(
        "Select Data Type:",
        available_data_types,
        index=available_data_types.index(st.session_state["data_type"]),
        key="data_type_radio"
    )
    st.session_state["data_type"] = selected_data_type

    # Load and display Meta File
    if selected_data_type == "Meta":
        st.write("### Metadata Overview")
        meta_data = load_meta_file(meta_file)
        if not meta_data.empty:
            st.dataframe(meta_data)
            return meta_data
        else:
            st.error("Metadata file not found.")

    # Load and display Stocks Data
    elif selected_data_type == "Stocks":
        stock_files = list_csv_files(stocks_dir)
        selected_stock = st.sidebar.selectbox("Select Stock:", stock_files, key="selected_stock")
        if selected_stock:
            stock_data = load_stock_data(stocks_dir, selected_stock)
            st.write(f"### Stock Data: {selected_stock}")
            st.dataframe(stock_data)
            return stock_data

    # Load and display ETFs Data
    elif selected_data_type == "ETFs":
        etf_files = list_csv_files(etfs_dir)
        selected_etf = st.sidebar.selectbox("Select ETF:", etf_files, key="selected_etf")
        if selected_etf:
            etf_data = load_stock_data(etfs_dir, selected_etf)
            st.write(f"### ETF Data: {selected_etf}")
            st.dataframe(etf_data)
            return etf_data

    st.warning("No data available for the selected category.")
    return None

def get_available_files(directory):
    """
    Lists all CSV files in the given directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        list: List of CSV file names.
    """
    try:
        return [f for f in os.listdir(directory) if f.endswith(".csv")]
    except FileNotFoundError:
        return []
    except Exception as e:
        raise RuntimeError(f"Error accessing {directory}: {e}")

def load_csv_file(file_path):
    """
    Loads a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: The loaded data.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"Error loading {file_path}: {e}")

def load_meta_file(meta_file):
    """
    Loads the meta file as a DataFrame.
    
    Args:
        meta_file (str): Path to the meta file.
    
    Returns:
        DataFrame: Metadata as a Pandas DataFrame.
    """
    try:
        return pd.read_csv(meta_file)
    except Exception as e:
        st.error(f"Error loading meta file: {e}")
        return pd.DataFrame()


def list_csv_files(directory):
    """
    Lists all CSV files in a directory.
    
    Args:
        directory (str): Path to the directory.
    
    Returns:
        list: List of CSV file names.
    """
    try:
        return [f for f in os.listdir(directory) if f.endswith(".csv")]
    except Exception as e:
        st.error(f"Error accessing directory {directory}: {e}")
        return []


def load_stock_data(directory, file_name):
    """
    Loads a stock/ETF CSV file as a DataFrame.
    
    Args:
        directory (str): Path to the stocks or ETFs directory.
        file_name (str): Name of the CSV file.
    
    Returns:
        DataFrame: Stock/ETF data as a Pandas DataFrame.
    """
    file_path = os.path.join(directory, file_name)
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading file {file_name}: {e}")
        return pd.DataFrame()
