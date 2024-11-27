
# elif page == "Sector-SP500 Correlation":
#     st.header("Sector Correlation with S&P 500")
#     st.write("Analyze how different sectors correlate with the S&P 500 index")
    
#     # Get sector data
#     sector, stock_data, tickers, start_date, end_date = get_sector_data()
    
#     # Get S&P 500 data for the same period
#     sp500_data = yf.download('^GSPC', start=start_date, end=end_date)
    
#     if not stock_data.empty and not sp500_data.empty:
#         # Calculate daily returns
#         sector_returns = stock_data['Close'].pct_change()
#         sp500_returns = sp500_data['Close'].pct_change()
        
#         # Calculate correlations
#         correlations = {}
#         for ticker in tickers:
#             corr = sector_returns[ticker].corr(sp500_returns)
#             correlations[ticker] = corr
        
#         # Create correlation plot
#         fig = px.bar(x=list(correlations.keys()), 
#                     y=list(correlations.values()),
#                     title=f'Correlation with S&P 500')
#         st.plotly_chart(fig)

# else:  # Price Prediction
#     st.header("Stock Price Prediction")
#     st.write("Predict future stock prices based on historical data")
    
#     # Get data
#     sector, stock_data, tickers, start_date, end_date = get_sector_data()
    
#     if not stock_data.empty:
#         selected_stock = st.selectbox("Select a stock for price prediction:", tickers)
        
#         # Get stock data
#         stock_prices = stock_data['Close'][selected_stock]
        
#         # Calculate moving averages
#         ma20 = stock_prices.rolling(window=20).mean()
#         ma50 = stock_prices.rolling(window=50).mean()
        
#         # Create prediction plot
#         fig = px.line(title=f'Price Prediction Analysis for {selected_stock}')
#         fig.add_scatter(x=stock_prices.index, y=stock_prices, name='Actual Price')
#         fig.add_scatter(x=ma20.index, y=ma20, name='20-day MA')
#         fig.add_scatter(x=ma50.index, y=ma50, name='50-day MA')
#         st.plotly_chart(fig)
        
#         # Simple future price prediction
#         last_price = stock_prices.iloc[-1]
#         growth_rate = (stock_prices.iloc[-1] / stock_prices.iloc[0]) ** (1/len(stock_prices)) - 1
        
#         days_to_predict = st.slider("Number of days to predict:", 1, 30, 7)
#         predicted_price = last_price * (1 + growth_rate) ** days_to_predict
        
#         st.write(f"Predicted price after {days_to_predict} days: ${predicted_price:.2f}")
#         st.write(f"Current price: ${last_price:.2f}")
#         st.write(f"Predicted change: {((predicted_price/last_price - 1) * 100):.2f}%")

