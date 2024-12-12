import pandas as pd
import os

# Load raw data
def load_raw_data(filepath):
    """
    Load raw inventory data from a CSV file.
    
    Parameters:
    - filepath: Path to the raw data file.

    Returns:
    - DataFrame containing the raw data.
    """
    print(f"Loading raw data from {filepath}...")
    data = pd.read_csv(filepath)
    return data

# Clean and preprocess data
def clean_data(data):
    """
    Clean and preprocess raw inventory data.

    Parameters:
    - data: DataFrame containing raw inventory data.

    Returns:
    - Cleaned DataFrame.
    """
    print("Cleaning data...")
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')

    # Ensure date column is in datetime format
    data['date'] = pd.to_datetime(data['date'], errors='coerce')

    # Drop rows with missing or invalid dates
    data = data.dropna(subset=['date'])

    # Sort by date
    data = data.sort_values('date')

    # Handle missing values in demand column
    data['demand'] = data['demand'].fillna(0)

    print("Data cleaning completed.")
    return data

# Aggregate data if needed
def aggregate_data(data, freq='D'):
    """
    Aggregate inventory data to the specified frequency.

    Parameters:
    - data: DataFrame containing cleaned inventory data.
    - freq: Aggregation frequency (e.g., 'D' for daily, 'W' for weekly).

    Returns:
    - Aggregated DataFrame.
    """
    print(f"Aggregating data to {freq} frequency...")
    data = data.set_index('date')
    aggregated_data = data.resample(freq).sum().reset_index()
    print("Aggregation completed.")
    return aggregated_data

# Save processed data
def save_processed_data(data, output_path):
    """
    Save processed data to a CSV file.

    Parameters:
    - data: DataFrame containing processed inventory data.
    - output_path: Path to save the processed data.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    # File paths
    raw_data_filepath = "data/raw/inventory_data.csv"
    processed_data_filepath = "data/processed/historical_inventory.csv"

    # Load raw data
    raw_data = load_raw_data(raw_data_filepath)

    # Clean and preprocess data
    cleaned_data = clean_data(raw_data)

    # Aggregate data (daily frequency)
    aggregated_data = aggregate_data(cleaned_data, freq='D')

    # Save processed data
    save_processed_data(aggregated_data, processed_data_filepath)
