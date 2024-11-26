import streamlit as st

def home_page():
    """
    Displays the Home page for the app.
    Includes an introduction, navigation instructions, and an overview of app features.
    """
    # Add About section to sidebar
    with st.sidebar:
        st.write("""
        ### About This App
        This app provides tools for analyzing stock market trends and building predictive models.
        Navigate through the pages to explore different features, including regression analysis, 
        sector correlations, and price predictions.
        """)

    st.write("""
    ### Navigation
    Use the sidebar to switch between the following sections:
    - **Home**: Overview of the app and its features.
    - **Regression Analysis**: Explore relationships between stock features and their prices.
    - **Sector-SP500 Correlation**: Analyze how sectors correlate with the S&P 500 index.
    - **Price Prediction**: Predict future stock prices.
    """)

    st.write("""
    ### Key Features
    - Intuitive interface for sector-based analysis.
    - Dynamic regression modeling tools.
    - Predictive insights into stock trends.
    - Explore correlations between sectors and the broader market.
    """)

    st.write("### Get Started")
    st.info("Navigate to any section using the sidebar to begin your analysis.")

# Example usage
if __name__ == "__main__":
    home_page()
