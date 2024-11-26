from lib.kaggle_data import fetch_kaggle_data

def render_data_selector_kaggle():
    """
    Renders the dataset selector for the app.
    Allows users to choose stocks and filter data by date range.
    
    Returns:
        DataFrame: The filtered dataset based on user selections.
    """
    st.sidebar.title("Dataset Selector")

    # File options (files available in the Kaggle dataset)
    stock_options = ["AAPL.csv", "MSFT.csv", "GOOGL.csv"]

    # Multiselect for stocks
    selected_stocks = st.sidebar.multiselect("Select Stocks:", stock_options)

    # Date range filters
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))

    # Load and filter data
    if selected_stocks:
        combined_data = []
        for stock in selected_stocks:
            df = fetch_kaggle_data(stock)
            df["Date"] = pd.to_datetime(df["Date"])
            filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
            combined_data.append(filtered_df)
        data = pd.concat(combined_data, axis=0)
        st.write(f"Loaded Data for {', '.join(selected_stocks)}")
        st.dataframe(data)
        return data
    else:
        st.write("Select at least one stock to view data.")
        return None
