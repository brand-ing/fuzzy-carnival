import os
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
from lib.kaggle_data import TEMP_DIR
from lib.data_loader import get_available_files, load_csv_file


def regression_page():
    """
    Regression page workflow:
    1. Load data from Kaggle (if not already loaded).
    2. Select category (Stocks or ETFs).
    3. Select a specific CSV file for regression analysis.
    """
    st.title("Regression Analysis")

    # Initialize session state
    if "loaded_data" not in st.session_state:
        st.session_state["loaded_data"] = None
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = "Stocks"
    if "selected_file" not in st.session_state:
        st.session_state["selected_file"] = None

    # Step 1: Load data from Kaggle
    if st.sidebar.button("Load Dataset from Kaggle"):
        with st.spinner("Loading data from Kaggle..."):
            # Simulate fetching Kaggle data (TEMP_DIR should be preconfigured)
            st.success("Dataset loaded successfully!")
            st.session_state["loaded_data"] = TEMP_DIR

    # Check if data is loaded
    if not st.session_state["loaded_data"]:
        st.warning("Please load the dataset from Kaggle first.")
        return

    # Step 2: Select category (Stocks or ETFs)
    st.sidebar.title("Data Category")
    st.session_state["selected_category"] = st.sidebar.radio(
        "Select Category:", ["Stocks", "ETFs"], index=0
    )

    # Step 3: Select specific CSV file
    st.sidebar.title("File Selector")
    category_dir = os.path.join(TEMP_DIR, st.session_state["selected_category"].lower())
    available_files = get_available_files(category_dir)
    if not available_files:
        st.warning(f"No files available in {st.session_state['selected_category']} category.")
        return

    st.session_state["selected_file"] = st.sidebar.selectbox(
        "Select a file:", available_files
    )

    # Step 4: Load and display selected CSV
    selected_file = st.session_state["selected_file"]
    if selected_file:
        file_path = os.path.join(category_dir, selected_file)
        data = load_csv_file(file_path)
        st.write(f"### Data from {selected_file}")
        st.dataframe(data.head())

        # Step 5: Perform regression analysis
        if st.button("Run Regression"):
            run_regression(data)


def run_regression(data):
    """
    Perform regression analysis on the selected dataset.
    """
    # Prepare data for regression
    if "Close" not in data.columns or "Date" not in data.columns:
        st.error("Dataset must contain 'Date' and 'Close' columns for regression.")
        return

    data = data.sort_values(by="Date")
    data["Days"] = range(len(data))

    X = data[["Days"]]
    y = data["Close"]

    # Fit regression model
    model = LinearRegression()
    model.fit(X, y)

    # Make predictions
    data["Predicted"] = model.predict(X)

    # Create plot
    fig = px.line(data, x="Date", y=["Close", "Predicted"], title="Regression Analysis")
    st.plotly_chart(fig)

    # Show regression metrics
    st.write(f"Slope: {model.coef_[0]:.2f}")
    st.write(f"R² Score: {model.score(X, y):.4f}")
