import sklearn.preprocessing as preprocessing
import pandas as pd

def date_preprocessing(df):
    # Assuming df['date'] is your date column
    df['Date'] = pd.to_datetime(df['Date'])
    df['day_of_week'] = df['Date'].dt.dayofweek # Extract day of week (0=Monday, 6=Sunday)
    df['month'] = df['Date'].dt.month          # Extract month (1-12)
    df['quarter'] = df['Date'].dt.quarter       # Extract quarter (1-4)

    # Ordinal encode 'month' and 'quarter' as ordered features
    ordinal_encoder = OrdinalEncoder()
    df[['month', 'quarter']] = ordinal_encoder.fit_transform(df[['month', 'quarter']])
    df.drop(columns=['Date'], inplace=True)
    X = df.drop(columns=['Adj Close'])  # Assuming 'adj_close' is your target
    y = df['Adj Close']
    return X, y


