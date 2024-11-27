from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

def run_model_pipeline(data, features, target, test_size=0.2, random_state=1):
    """
    Runs the complete model pipeline: preprocessing, training, and evaluation.
    
    Args:
        data (DataFrame): Input dataset.
        features (list): Selected feature columns.
        target (str): Target column.
        test_size (float): Proportion of data to use for testing.
        random_state (int): Random seed for reproducibility.
    
    Returns:
        dict: Dictionary containing model, predictions, and evaluation metrics.
    """
    # Train/test split
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate model
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return {
        "model": model,
        "X_test": X_test,
        "y_test": y_test,
        "predictions": predictions,
        "mse": mse,
        "r2": r2
    }
