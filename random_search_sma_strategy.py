import random
import numpy as np
from sma_strategy import sma_strategy  # Ensure this is imported


def random_search_sma_strategy(backtest_func, num_trials=100):
    best_sharpe = -np.inf
    best_params = None

    for _ in range(num_trials):
        # Randomly sample parameters
        short_window = random.randint(10, 50)
        long_window = random.randint(50, 200)
        volume_threshold = random.uniform(1.0, 3.0)
        rsi_period = random.randint(10, 20)
        rsi_threshold = random.randint(20, 40)

        # Pass the sampled parameters to the backtest function
        results = backtest_func(
            strategy_func=sma_strategy,
            ticker='AAPL',
            short_window=short_window,
            long_window=long_window,
            use_volume=True,
            volume_threshold=volume_threshold,
            use_rsi=True,
            rsi_period=rsi_period,
            rsi_threshold=rsi_threshold
        )

        # Track the best result based on Sharpe Ratio
        if results['Sharpe Ratio'] > best_sharpe:
            best_sharpe = results['Sharpe Ratio']
            best_params = {
                'short_window': short_window,
                'long_window': long_window,
                'volume_threshold': volume_threshold,
                'rsi_period': rsi_period,
                'rsi_threshold': rsi_threshold
            }

    print(f"Best Sharpe Ratio: {best_sharpe}")
    print(f"Best Parameters: {best_params}")
    return best_params

