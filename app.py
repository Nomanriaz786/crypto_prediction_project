
from src.data_pipeline.ingestion.ccxt_data_fetcher import DataIngestion


if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion.download_historical_data()