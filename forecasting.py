import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os

# Load and preprocess data
def load_data(filepath):
    data = pd.read_csv(filepath)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    return data

# Save forecasts to a CSV file
def save_forecasts(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path)

# Generate forecasts using Exponential Smoothing
def generate_forecasts(data, column, forecast_periods, seasonal_periods):
    print("Training model...")
    model = ExponentialSmoothing(
        data[column],
        seasonal="add",
        seasonal_periods=seasonal_periods,
        trend="add"
    ).fit()

    print("Generating forecasts...")
    forecasts = model.forecast(forecast_periods)
    data['Forecast'] = model.fittedvalues
    future_dates = pd.date_range(start=data.index[-1], periods=forecast_periods + 1, freq="D")[1:]
    future_forecasts = pd.DataFrame({
        'Date': future_dates,
        'Forecast': forecasts
    })

    future_forecasts.set_index('Date', inplace=True)
    return pd.concat([data, future_forecasts])

# Calculate forecast accuracy
def calculate_accuracy(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    return mae, rmse, mape

if __name__ == "__main__":
    # File paths
    input_filepath = "data/processed/historical_inventory.csv"
    output_filepath = "data/processed/forecasted_inventory.csv"

    # Load data
    print("Loading data...")
    data = load_data(input_filepath)

    # Generate forecasts
    forecast_periods = 30  # Number of days to forecast
    seasonal_periods = 12  # Monthly seasonality (if daily data spans multiple months)

    forecasted_data = generate_forecasts(data, column="Demand", forecast_periods=forecast_periods, seasonal_periods=seasonal_periods)

    # Calculate forecast accuracy
    actual = data["Demand"]
    predicted = data["Forecast"].dropna()

    mae, rmse, mape = calculate_accuracy(actual[-len(predicted):], predicted)
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

    # Save forecasts
    print("Saving forecasted data...")
    save_forecasts(forecasted_data, output_filepath)
    print(f"Forecasts saved to {output_filepath}")
