import random
import numpy as np
from momentum_strategy import momentum_strategy  # Ensure this is imported


def random_search_momentum_strategy(backtest_func, num_trials=100):
    best_sharpe = -np.inf
    best_params = None

    for _ in range(num_trials):
        # Randomly sample parameters
        lookback = random.randint(10, 50)
        volatility_threshold = random.uniform(0.01, 0.05)
        macd_fast = random.randint(8, 12)
        macd_slow = random.randint(18, 26)
        macd_signal = random.randint(5, 9)
        volume_threshold = random.uniform(1.0, 3.0)

        # Pass the sampled parameters to the backtest function
        results = backtest_func(
            strategy_func=momentum_strategy,
            ticker='AAPL',
            lookback=lookback,
            volatility_threshold=volatility_threshold,
            use_macd=True,
            macd_fast=macd_fast,
            macd_slow=macd_slow,
            macd_signal=macd_signal,
            use_volume=True,
            volume_threshold=volume_threshold
        )

        # Track the best result based on Sharpe Ratio
        if results['Sharpe Ratio'] > best_sharpe:
            best_sharpe = results['Sharpe Ratio']
            best_params = {
                'lookback': lookback,
                'volatility_threshold': volatility_threshold,
                'macd_fast': macd_fast,
                'macd_slow': macd_slow,
                'macd_signal': macd_signal,
                'volume_threshold': volume_threshold
            }

    print(f"Best Sharpe Ratio: {best_sharpe}")
    print(f"Best Parameters: {best_params}")
    return best_params

