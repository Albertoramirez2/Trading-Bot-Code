import numpy as np


def apply_stop_loss_take_profit(df, stop_loss=0.02, take_profit=0.05):
    """
    Apply stop-loss and take-profit conditions to the strategy.

    :param df: DataFrame with stock data and signals.
    :param stop_loss: Stop-loss threshold as a percentage.
    :param take_profit: Take-profit threshold as a percentage.
    :return: DataFrame with stop-loss and take-profit applied.
    """
    entry_price = df['close'].shift(1)
    df['stop_loss'] = np.where(df['close'] < entry_price * (1 - stop_loss), -1, 0)
    df['take_profit'] = np.where(df['close'] > entry_price * (1 + take_profit), 1, 0)
    df['exit_signal'] = np.where(df['stop_loss'] | df['take_profit'], -1, df['position'])
    return df
