# mean_reversion.py

import numpy as np


def mean_reversion_strategy(df, lookback, deviation, use_rsi=False, rsi_period=14, rsi_threshold=30):
    # Calculate the mean and standard deviation
    df['mean'] = df['close'].rolling(window=lookback).mean()
    df['std_dev'] = df['close'].rolling(window=lookback).std()

    # Optional RSI calculation
    if use_rsi:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

    # Generate signals using a more dynamic approach
    df['signal_Mean Reversion'] = 0
    df['signal_Mean Reversion'] = np.where(
        (df['close'] < df['mean'] - deviation * df['std_dev']) &
        ((df['RSI'] < rsi_threshold) if use_rsi else True),
        1, df['signal_Mean Reversion']
    )
    df['signal_Mean Reversion'] = np.where(
        (df['close'] > df['mean'] + deviation * df['std_dev']) &
        ((df['RSI'] > 100 - rsi_threshold) if use_rsi else True),
        -1, df['signal_Mean Reversion']
    )

    # Shift signals for realistic backtesting
    df['position'] = df['signal_Mean Reversion'].shift(1)

    return df
