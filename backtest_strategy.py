import pandas as pd
import numpy as np
from fetch_and_store_data import fetch_and_store_data


def backtest_strategy(strategy_func, ticker, **strategy_params):
    """
    Backtest a given trading strategy.

    :param strategy_func: The strategy function to apply (e.g., sma_strategy, mean_reversion_strategy)
    :param ticker: The stock ticker to backtest on
    :param strategy_params: The parameters to pass to the strategy function
    :return: A DataFrame containing performance metrics and combined outputs
    """
    # Fetch the historical data for the given ticker
    df = fetch_data(ticker)

    # Apply the trading strategy
    df = strategy_func(df, **strategy_params)

    # Initialize portfolio values
    initial_cash = 100000  # Starting cash for the backtest
    df['position'] = df['position'].fillna(0)  # Ensure no NaNs in positions
    df['cash'] = initial_cash
    df['holdings'] = 0.0  # Ensure float dtype for holdings
    df['total_asset'] = initial_cash

    # Simulate trading
    for i in range(1, len(df)):
        df.at[i, 'holdings'] = float(df['position'].iloc[i] * df['close'].iloc[i])
        df.at[i, 'cash'] = float(
            df['cash'].iloc[i - 1] - (df['position'].iloc[i] - df['position'].iloc[i - 1]) * df['close'].iloc[i])
        df.at[i, 'total_asset'] = float(df['cash'].iloc[i] + df['holdings'].iloc[i])

    # Calculate performance metrics
    total_trades = df['position'].diff().abs().sum()
    total_return = df['total_asset'].iloc[-1] - initial_cash
    annualized_return = (total_return / initial_cash) / len(df) * 252  # Assuming 252 trading days in a year

    pct_changes = df['total_asset'].pct_change()
    sharpe_ratio = (pct_changes.mean() / pct_changes.std()) * np.sqrt(252) if pct_changes.std() > 0 else np.nan
    max_drawdown = (df['total_asset'].cummax() - df['total_asset']).max()

    # Add performance metrics to the DataFrame
    df['Total Trades'] = total_trades
    df['Total Return'] = total_return
    df['Annualized Return'] = annualized_return
    df['Sharpe Ratio'] = sharpe_ratio
    df['Max Drawdown'] = max_drawdown

    # Return the DataFrame with all the combined outputs
    return df

# Example usage:
# result = backtest_strategy(sma_strategy, 'AAPL', short_window=40, long_window=100)
