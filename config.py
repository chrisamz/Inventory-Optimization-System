import os

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "inventory_db")
}

# File paths
DATA_PATHS = {
    "raw_data": os.getenv("RAW_DATA_PATH", "data/raw"),
    "processed_data": os.getenv("PROCESSED_DATA_PATH", "data/processed"),
    "dashboard_templates": os.getenv("DASHBOARD_TEMPLATES_PATH", "dashboards")
}

# Application settings
APP_SETTINGS = {
    "secret_key": os.getenv("SECRET_KEY", "your_secret_key"),
    "debug": os.getenv("DEBUG", "True").lower() in ("true", "1", "yes"),
    "host": os.getenv("APP_HOST", "127.0.0.1"),
    "port": int(os.getenv("APP_PORT", 8050))
}

# Logging configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": os.getenv("LOG_FILE", "app.log")
}

# Forecasting model parameters
FORECASTING_PARAMS = {
    "seasonality": int(os.getenv("SEASONALITY", "12")),
    "confidence_interval": float(os.getenv("CONFIDENCE_INTERVAL", "0.95"))
}

if __name__ == "__main__":
    print("Database Configuration:")
    print(DB_CONFIG)
    print("Data Paths:", DATA_PATHS)
    print("App Settings:", APP_SETTINGS)
    print("Logging Config:", LOGGING_CONFIG)
    print("Forecasting Params:", FORECASTING_PARAMS)
