# sma_strategy.py

import pandas as pd
import numpy as np


def sma_strategy(df, short_window, long_window, use_volume=False, volume_threshold=1.5, use_rsi=False, rsi_period=14,
                 rsi_threshold=30):
    """
    Implements a SMA crossover strategy with optional volume and RSI confirmation.

    :param df: pandas.DataFrame containing 'close' prices and optionally 'volume'
    :param short_window: lookback period for the short SMA
    :param long_window: lookback period for the long SMA
    :param use_volume: whether to use volume as a confirmation indicator
    :param volume_threshold: threshold multiplier for volume confirmation
    :param use_rsi: whether to use RSI as a confirmation indicator
    :param rsi_period: RSI period for calculation
    :param rsi_threshold: RSI threshold for overbought/oversold signals
    :return: pandas.DataFrame with signals and positions
    """
    df['short_sma'] = df['close'].rolling(window=short_window).mean()
    df['long_sma'] = df['close'].rolling(window=long_window).mean()

    # Optional RSI calculation
    if use_rsi:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

    # Generate SMA crossover signals
    df['signal_SMA'] = 0
    df['signal_SMA'] = np.where(
        (df['short_sma'] > df['long_sma']) &
        ((df['volume'] > volume_threshold * df['volume'].rolling(short_window).mean()) if use_volume else True) &
        ((df['RSI'] < rsi_threshold) if use_rsi else True),
        1, df['signal_SMA']
    )
    df['signal_SMA'] = np.where(
        (df['short_sma'] < df['long_sma']) &
        ((df['volume'] > volume_threshold * df['volume'].rolling(short_window).mean()) if use_volume else True) &
        ((df['RSI'] > 100 - rsi_threshold) if use_rsi else True),
        -1, df['signal_SMA']
    )

    # Position sizing and trade execution logic
    df['position'] = df['signal_SMA'].shift(1)
    df['position'] = df['position'].fillna(0)

    return df
