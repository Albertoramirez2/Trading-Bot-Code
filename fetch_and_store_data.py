import yfinance as yf
import pandas as pd
import sqlite3
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)

def fetch_and_store_data(ticker, db_path='../data/trading_data.db', start_date="2020-01-01", end_date="2023-01-01"):
    """
    Fetch historical stock data for the given ticker from Yahoo Finance and store it in an SQLite database,
    ensuring the use of adjusted close prices and handling potential data issues.
    """
    logging.info(f"Fetching data for {ticker} from Yahoo Finance...")
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        logging.error(f"No data found for {ticker} from {start_date} to {end_date}.")
        return

    # Check for NaN values and print a summary of the data
    logging.info(f"Data Summary for {ticker}:")
    logging.info(df.info())
    if df.isnull().values.any():
        logging.warning(f"Data contains NaN values. Dropping NaNs for {ticker}.")
        df = df.dropna()

    # Ensure correct data types
    df = df[['Adj Close', 'Open', 'High', 'Low', 'Volume']].rename(columns={'Adj Close': 'Close'})
    df = df.astype({
        'Close': 'float64',
        'Open': 'float64',
        'High': 'float64',
        'Low': 'float64',
        'Volume': 'int64'
    })

    # Print the data to inspect it
    logging.info(f"Sample data for {ticker}:")
    logging.info(df.head())

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    try:
        logging.info(f"Storing data for {ticker} in {db_path}...")
        df.to_sql(ticker, conn, if_exists='replace', index=True)
        logging.info(f"Data for {ticker} stored successfully.")
    except Exception as e:
        logging.error(f"Error storing data: {e}")
    finally:
        conn.close()

# Example usage:
fetch_and_store_data('AAPL')
