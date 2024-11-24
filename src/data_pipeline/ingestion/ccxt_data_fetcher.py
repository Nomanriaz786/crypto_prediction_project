import os
import sys
import ccxt
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataIngestionConfig:
    raw_data_dir: str = os.path.join('data', 'raw')

class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()
        os.makedirs(self.config.raw_data_dir, exist_ok=True)
        self.binance = ccxt.binance()
        self.cryptos = ['BTC/USDT', 'ETH/USDT', 'BCH/USDT', 'SOL/USDT', 'LTC/USDT']
        self.timeframes = ['4h', '1d']

    def fetch_ohlcv(self, symbol, timeframe, since, limit=1000):
        """Fetch OHLCV data from Binance and return as a DataFrame."""
        try:
            ohlcv = self.binance.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self, df, symbol, timeframe):
        """Save the DataFrame to a CSV file."""
        try:
            coin_name = symbol.split('/')[0].lower()
            filename = f"{coin_name}_{timeframe}.csv"
            filepath = os.path.join(self.config.raw_data_dir, filename)
            
            if os.path.exists(filepath):
                existing_df = pd.read_csv(filepath)
                existing_df['timestamp'] = pd.to_datetime(existing_df['timestamp'])
                combined_df = pd.concat([existing_df, df]).drop_duplicates(subset='timestamp').sort_values(by='timestamp')
                if combined_df.equals(existing_df):
                    logging.info(f"No new data for {symbol} {timeframe}.")
                else:
                    combined_df.to_csv(filepath, index=False)
                    logging.info(f"Updated {symbol} {timeframe} data in {filepath}.")
            else:
                df.to_csv(filepath, index=False)
                logging.info(f"Saved new {symbol} {timeframe} data to {filepath}.")
        except Exception as e:
            raise CustomException(e, sys)

    def download_historical_data(self):
        """Download historical data for specified cryptocurrencies and timeframes."""
        try:
            for symbol in self.cryptos:
                for timeframe in self.timeframes:
                    since = self.binance.parse8601('2013-01-01T00:00:00Z')
                    now = datetime.now().timestamp() * 1000  # Convert to milliseconds
                    while since < now:
                        df = self.fetch_ohlcv(symbol, timeframe, since)
                        if df.empty:
                            break
                        self.save_data(df, symbol, timeframe)
                        since = int(df['timestamp'].iloc[-1].timestamp() * 1000) + 1
            logging.info("Data download completed.")
        except Exception as e:
            raise CustomException(e, sys)