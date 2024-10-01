import random
from mean_reversion import mean_reversion_strategy  # Ensure this is imported


def random_search_mean_reversion(backtest_func, num_trials=100):
    best_sharpe = -np.inf
    best_params = None

    for _ in range(num_trials):
        # Randomly sample parameters
        lookback = random.randint(10, 50)
        deviation = random.uniform(1.0, 3.0)
        rsi_period = random.randint(10, 20)
        rsi_threshold = random.randint(20, 40)

        # Pass the sampled parameters to the backtest function
        results = backtest_func(
            strategy_func=mean_reversion_strategy,
            ticker='AAPL',
            lookback=lookback,
            deviation=deviation,
            use_rsi=True,
            rsi_period=rsi_period,
            rsi_threshold=rsi_threshold
        )

        # Track the best result based on Sharpe Ratio
        if results['Sharpe Ratio'] > best_sharpe:
            best_sharpe = results['Sharpe Ratio']
            best_params = {
                'lookback': lookback,
                'deviation': deviation,
                'rsi_period': rsi_period,
                'rsi_threshold': rsi_threshold
            }

    print(f"Best Sharpe Ratio: {best_sharpe}")
    print(f"Best Parameters: {best_params}")
    return best_params

