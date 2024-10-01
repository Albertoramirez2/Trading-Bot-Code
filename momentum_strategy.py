# momentum_strategy.py

import pandas as pd
import numpy as np


def momentum_strategy(df, lookback=20, volatility_threshold=0.02,
                      use_macd=False, macd_fast=12, macd_slow=26, macd_signal=9,
                      use_volume=False, volume_threshold=1.5):
    """
    Implements a dynamic momentum strategy with optional MACD and volume confirmation.

    :param df: pandas.DataFrame containing 'close' prices and optionally 'volume'
    :param lookback: lookback period for momentum calculation
    :param volatility_threshold: volatility threshold to filter trades
    :param use_macd: whether to use MACD as a confirmation indicator
    :param macd_fast: fast period for MACD
    :param macd_slow: slow period for MACD
    :param macd_signal: signal line period for MACD
    :param use_volume: whether to use volume as a confirmation indicator
    :param volume_threshold: threshold multiplier for volume confirmation
    :return: pandas.DataFrame with signals and positions
    """
    df['momentum'] = df['close'].pct_change(lookback)
    df['volatility'] = df['close'].rolling(lookback).std()

    # Optional MACD calculation
    if use_macd:
        df['ema_fast'] = df['close'].ewm(span=macd_fast, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=macd_slow, adjust=False).mean()
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['macd_signal'] = df['macd'].ewm(span=macd_signal, adjust=False).mean()
        df['macd_diff'] = df['macd'] - df['macd_signal']

    # Generate dynamic momentum signals
    df['signal_Momentum'] = 0
    df['signal_Momentum'] = np.where(
        (df['momentum'] > 0) &
        (df['volatility'] < volatility_threshold) &
        ((df['macd_diff'] > 0) if use_macd else True) &
        ((df['volume'] > volume_threshold * df['volume'].rolling(lookback).mean()) if use_volume else True),
        1, df['signal_Momentum']
    )
    df['signal_Momentum'] = np.where(
        (df['momentum'] < 0) &
        (df['volatility'] < volatility_threshold) &
        ((df['macd_diff'] < 0) if use_macd else True) &
        ((df['volume'] > volume_threshold * df['volume'].rolling(lookback).mean()) if use_volume else True),
        -1, df['signal_Momentum']
    )

    # Position sizing and trade execution logic
    df['position'] = df['signal_Momentum'].shift(1)
    df['position'] = df['position'].fillna(0)

    return df
