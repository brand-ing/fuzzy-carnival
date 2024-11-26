import streamlit as st
from lib.data_selector import render_data_selector_kaggle


def regression_page():
    st.title("Regression Analysis")
    st.write("Build your own regression model here.")
    data = render_data_selector_kaggle()
    if data is not None:
        st.write("Ready to build your model?")

if __name__ == "__main__":
    regression_page()
    