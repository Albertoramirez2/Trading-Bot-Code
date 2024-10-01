import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sma_strategy import sma_strategy
from momentum_strategy import momentum_strategy
from mean_reversion_strategy import mean_reversion_strategy
from backtest_strategy import backtest_strategy


def run_all_strategies(ticker):
    # Run SMA Strategy
    print("Running SMA Strategy...")
    sma_result = backtest_strategy(
        strategy_func=sma_strategy,
        ticker=ticker,
        short_window=40,
        long_window=100
    )
    print(sma_result.head())

    # Run Momentum Strategy
    print("Running Momentum Strategy...")
    momentum_result = backtest_strategy(
        strategy_func=momentum_strategy,
        ticker=ticker,
        lookback=20,
        volatility_threshold=0.02,
        use_macd=True,
        macd_fast=12,
        macd_slow=26,
        macd_signal=9,
        use_volume=True,
        volume_threshold=1.5
    )
    print(momentum_result.head())

    # Run Mean Reversion Strategy
    print("Running Mean Reversion Strategy...")
    mean_reversion_result = backtest_strategy(
        strategy_func=mean_reversion_strategy,
        ticker=ticker,
        lookback=30,
        deviation=2,
        use_rsi=True,
        rsi_period=14,
        rsi_threshold=30
    )
    print(mean_reversion_result.head())

    # Plot the results
    plt.figure(figsize=(14, 7))
    plt.plot(sma_result['total_asset'], label="SMA Strategy")
    plt.plot(momentum_result['total_asset'], label="Momentum Strategy")
    plt.plot(mean_reversion_result['total_asset'], label="Mean Reversion Strategy")
    plt.title(f"Portfolio Value Over Time for {ticker}")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    ticker = 'AAPL'  # Change this to test other tickers
    run_all_strategies(ticker)
