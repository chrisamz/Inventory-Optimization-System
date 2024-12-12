import pandas as pd
import numpy as np
import os

# Load processed forecast data
def load_forecast_data(filepath):
    data = pd.read_csv(filepath)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Calculate reorder points and safety stock
def calculate_reorder_points(data, lead_time_days, service_level):
    """
    Calculate reorder points and safety stock for inventory items.

    Parameters:
    - data: DataFrame containing forecasted demand.
    - lead_time_days: Lead time in days for reordering stock.
    - service_level: Desired service level (e.g., 0.95 for 95%).

    Returns:
    - DataFrame with calculated reorder points and safety stock.
    """
    print("Calculating reorder points and safety stock...")

    # Daily demand standard deviation (assumes past demand variability is representative)
    data['Daily_Std_Dev'] = data['Demand'].rolling(window=lead_time_days).std()

    # Safety stock = Z * std_dev * sqrt(lead_time_days)
    z_score = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}[service_level]
    data['Safety_Stock'] = z_score * data['Daily_Std_Dev'] * np.sqrt(lead_time_days)

    # Reorder point = (Average Daily Demand * Lead Time) + Safety Stock
    data['Reorder_Point'] = (data['Demand'].rolling(window=lead_time_days).mean() * lead_time_days) + data['Safety_Stock']

    return data

# Save optimization results to CSV
def save_optimized_data(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path, index=False)

if __name__ == "__main__":
    # File paths
    input_filepath = "data/processed/forecasted_inventory.csv"
    output_filepath = "data/processed/optimized_inventory.csv"

    # Load forecast data
    print("Loading forecasted data...")
    forecast_data = load_forecast_data(input_filepath)

    # Parameters for optimization
    lead_time_days = 7  # Example: average lead time is 7 days
    service_level = 0.95  # Desired service level (95%)

    # Calculate reorder points and safety stock
    optimized_data = calculate_reorder_points(forecast_data, lead_time_days, service_level)

    # Save results
    print("Saving optimized inventory data...")
    save_optimized_data(optimized_data, output_filepath)
    print(f"Optimized data saved to {output_filepath}")
