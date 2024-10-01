def fetch_data(ticker, db_path='../data/trading_data.db'):
    """
    Fetch historical stock data from SQLite database.
    """
    conn = sqlite3.connect(db_path)

    try:
        logging.info(f"Fetching data for {ticker} from {db_path}...")
        df = pd.read_sql(f"SELECT * FROM {ticker}", conn, index_col='Date', parse_dates=['Date'])
        logging.info(f"Data for {ticker} fetched successfully.")
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    finally:
        conn.close()


# Example usage:
df = fetch_data('AAPL')
print(df.head())
