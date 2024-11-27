import os
import pandas as pd
import streamlit as st
from lib.data_loader import load_csv_file, TEMP_DIR
import yfinance as yf




def sector_analysis_page():
    """
    Sector Feature Builder for Neural Network:
    1. Allow users to define custom sectors by selecting stocks.
    2. Aggregate sector performance.
    3. Export sector features for modeling.
    """


    st.title("Sector Feature Builder")

    # Step 1: Load Preloaded Data
    sector_dir = os.path.join(TEMP_DIR, "stocks")
    sp500_file = os.path.join(sector_dir, "SPY.csv")  # Define the path to SPY.csv

    # Download SPY data if not already present
    if not os.path.exists(sp500_file):
        st.info("Downloading SPY data as the S&P 500 proxy...")
        spy_data = yf.download("SPY", start="1980-01-01", end="2023-01-01")
        os.makedirs(sector_dir, exist_ok=True)  # Ensure the directory exists
        spy_data.to_csv(sp500_file)
        st.success("SPY data downloaded and saved successfully!")

    # Check if stock data exists
    if not os.path.exists(sector_dir) or not os.listdir(sector_dir):
        st.warning("Stock data not available. Please ensure the data is preloaded.")
        return

    # Check if SPY data exists
    if not os.path.exists(sp500_file):
        st.warning("SPY data not available. Please ensure it is preloaded or downloaded.")
        return

    # Step 2: Stock Selection for Custom Sector
    sector_files = [f for f in os.listdir(sector_dir) if f.endswith(".csv")]
    selected_stocks = st.sidebar.multiselect(
        "Select Stocks for Custom Sector:", sector_files
    )

    if not selected_stocks:
        st.info("Please select at least one stock to define a sector.")
        return

    # Step 3: Aggregate Selected Stocks into Sector Feature
    sector_data = aggregate_sector_data(sector_dir, selected_stocks)
    st.write("### Custom Sector Performance")
    st.dataframe(sector_data.head())

    # Step 4: Export Sector Features
    if st.button("Export Features"):
        sector_feature = prepare_feature_for_modeling(sector_data)
        st.write("### Exported Feature for Neural Network")
        st.dataframe(sector_feature.head())
        st.success("Feature exported successfully!")

    # Optional: Add S&P 500 comparison
    if st.checkbox("Compare Sector to S&P 500"):
        sp500_data = load_csv_file(sp500_file)
        sp500_data["Date"] = pd.to_datetime(sp500_data["Date"])
        comparison = compare_to_sp500(sector_data, sp500_data)
        st.write("### Sector vs. S&P 500")
        st.dataframe(comparison)
        plot_sector_vs_sp500(comparison)


def aggregate_sector_data(sector_dir, selected_files):
    """
    Aggregates selected stock data into a custom sector index.

    Args:
        sector_dir (str): Directory containing stock data.
        selected_files (list): List of selected stock CSV files.

    Returns:
        DataFrame: Aggregated sector data.
    """
    sector_data = []
    for file in selected_files:
        file_path = os.path.join(sector_dir, file)
        stock_data = load_csv_file(file_path)
        stock_data["Date"] = pd.to_datetime(stock_data["Date"])
        sector_data.append(stock_data)

    combined_data = pd.concat(sector_data)
    aggregated_data = combined_data.groupby("Date")["Close"].mean().reset_index()
    aggregated_data.rename(columns={"Close": "Sector_Index"}, inplace=True)
    return aggregated_data


def prepare_feature_for_modeling(sector_data):
    """
    Prepares the sector data as a feature for the neural network.

    Args:
        sector_data (DataFrame): Aggregated sector data.

    Returns:
        DataFrame: Sector data formatted for modeling.
    """
    sector_data["Sector_Index_Norm"] = (sector_data["Sector_Index"] - sector_data["Sector_Index"].mean()) / sector_data["Sector_Index"].std()
    return sector_data[["Date", "Sector_Index_Norm"]]


def compare_to_sp500(sector_data, sp500_data):
    """
    Compares the sector performance to the S&P 500.

    Args:
        sector_data (DataFrame): Aggregated sector performance.
        sp500_data (DataFrame): S&P 500 performance.

    Returns:
        DataFrame: Comparison of sector and S&P 500 data.
    """
    merged_data = pd.merge(sector_data, sp500_data, on="Date", how="inner")
    merged_data.rename(columns={"Close": "SP500_Index"}, inplace=True)
    merged_data["Correlation"] = merged_data["Sector_Index"].corr(merged_data["SP500_Index"])
    return merged_data


def plot_sector_vs_sp500(comparison_df):
    """
    Plots the sector performance against the S&P 500.

    Args:
        comparison_df (DataFrame): Comparison of sector and S&P 500 data.
    """
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=comparison_df["Date"],
            y=comparison_df["Sector_Index"],
            mode="lines",
            name="Sector Index",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=comparison_df["Date"],
            y=comparison_df["SP500_Index"],
            mode="lines",
            name="S&P 500 Index",
        )
    )
    fig.update_layout(
        title="Sector vs. S&P 500 Performance",
        xaxis_title="Date",
        yaxis_title="Index Value",
    )
    st.plotly_chart(fig)
