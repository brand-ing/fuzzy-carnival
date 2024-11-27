import streamlit as st
import yfinance as yf
import plotly.express as px


import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from lib.home import home_page
from lib.regression_page import regression_page
from lib.sector_analysis_page import sector_analysis_page
from lib.render_prediction import render_prediction

# Set page config
st.set_page_config(page_title="TICKER", page_icon=":chart_with_upwards_trend:")
# App Title
st.title("TICKER: The Dynamic Market Prediction Tool")

# Create navigation menu in sidebar
PAGES = {
    "Home": home_page,
    "Regression Analysis": regression_page,
    "Sector-SP500 Correlation": sector_analysis_page,
    "Price Prediction": render_prediction,
}

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Render the selected page
page = PAGES[selection]
page()


