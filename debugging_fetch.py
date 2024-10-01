import yfinance as yf
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def fetch_data_debug(ticker, start_date="2020-01-01", end_date="2023-01-01"):
    logging.info(f"Fetching data for {ticker} from Yahoo Finance...")

    try:
        # Fetch data
        df = yf.download(ticker, start=start_date, end=end_date)
        logging.info("Data fetched successfully.")
        logging.info(df.head())

        # Check if 'Adj Close' is in the DataFrame
        if 'Adj Close' not in df.columns:
            raise KeyError("'Adj Close' column is missing from the data.")

        # Renaming and selecting specific columns
        df = df[['Adj Close', 'Open', 'High', 'Low', 'Volume']].rename(columns={'Adj Close': 'Close'})
        logging.info("Columns selected and renamed successfully.")

        # Convert data types
        df['Close'] = df['Close'].astype(float)
        df['Open'] = df['Open'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Volume'] = df['Volume'].astype(int)

        logging.info("Data types converted successfully.")
        logging.info(df.dtypes)

    except KeyError as ke:
        logging.error(f"Key error: {ke}")
    except ValueError as ve:
        logging.error(f"Value error: {ve}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise  # Re-raise the error after logging

    return df


# Test with a different ticker or date range if needed
try:
    df = fetch_data_debug('AAPL')
except Exception as final_error:
    logging.error(f"Final error encountered: {final_error}")
