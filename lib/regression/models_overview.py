import streamlit as st
import pandas as pd

def get_model_summaries():
    """
    Returns a DataFrame summarizing the traditional models and their metrics.
    """
    data = {
        "Model Name": ["Linear Regression", "Decision Tree", "Random Forest"],
        "R² Score": [0.85, 0.82, 0.88],
        "MSE": [12.34, 15.67, 10.45],
        "Sample Prediction": [102.3, 100.5, 103.8]  # Example predictions
    }
    return pd.DataFrame(data)

def render_models_overview():
    """
    Renders the models overview page in Streamlit.
    """
    st.title("Traditional Models Overview")

    # Fetch model summaries
    model_summaries = get_model_summaries()

    # Display the table
    st.write("### Model Performance Summary")
    st.dataframe(model_summaries)

    # Provide details for each model
    st.write("### Explore Models")
    for _, row in model_summaries.iterrows():
        with st.expander(f"{row['Model Name']} Details"):
            st.write(f"**R² Score**: {row['R² Score']}")
            st.write(f"**MSE**: {row['MSE']}")
            st.write(f"**Sample Prediction**: {row['Sample Prediction']}")
