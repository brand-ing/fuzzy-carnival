import streamlit as st
import yfinance as yf
import plotly.express as px


import seaborn as sns
import matplotlib.pyplot as plt



from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

# App Title
st.title("TICKER: The Dynamic Market Prediction Tool")

# Sidebar for Sector Selection
sectors = {
    "All": ["AAPL", "MSFT", "GOOGL", "JNJ", "PFE", "MRK", "XOM", "CVX", "BP"],
    "Tech": ["AAPL", "MSFT", "GOOGL"],
    "Healthcare": ["JNJ", "PFE", "MRK"],
    "Energy": ["XOM", "CVX", "BP"]
}


sector = st.sidebar.selectbox("Select a Sector:", list(sectors.keys()))
st.write(f"Sector: {sector} ")

# Fetch Sector Data
tickers = sectors[sector]
data = yf.download(tickers, start="2020-01-01", end="2023-01-01")

# Individual Stock Data
stock_ticker = st.sidebar.selectbox("Select a Stock Ticker:", sectors[sector])


# Calculate Average Close Price
avg_price = data["Close"].mean(axis=1)

# Plot Historical Trend
st.write("### Historical Trend")
fig = px.line(avg_price, title=f"{sector} Sector Performance", labels={"value": "Price", "index": "Date"})
st.plotly_chart(fig)


# You can also use "with" notation:
with tab1:
    st.radio("Select one:", [1, 2])


# Fetch S&P 500 Data
sp500 = yf.download("^GSPC", start="2020-01-01", end="2023-01-01")["Close"]

# Calculate Correlations
correlations = data["Close"].corrwith(sp500)

# Plot Correlation as Bar Chart
st.write("### Sector to S&P 500 Correlation")
sns.barplot(x=correlations.index, y=correlations.values)
plt.title("Correlation with S&P 500")
st.pyplot(plt.gcf())



# Prepare Data for Prediction
X = np.arange(len(avg_price)).reshape(-1, 1)
y = avg_price.values
model = LinearRegression()
model.fit(X, y)

# Predict Future Values
future_days = np.arange(len(avg_price), len(avg_price) + 30).reshape(-1, 1)
predictions = model.predict(future_days)

# Plot Predictions
st.write("### Predicted Trends")
future_dates = pd.date_range(avg_price.index[-1], periods=30, freq="B")
predicted_data = pd.DataFrame({"Date": future_dates, "Predicted Price": predictions})
fig = px.line(predicted_data, x="Date", y="Predicted Price", title="Future Sector Trend")
st.plotly_chart(fig)
