import numpy as np
import pandas as pd


def log_returns(prices):
    return np.log(prices / prices.shift(1)).dropna()


def historical_var(returns, confidence=0.95):
    return abs(np.percentile(returns, (1 - confidence) * 100))


def cvar(returns, confidence=0.95):
    var_threshold = np.percentile(returns, (1 - confidence) * 100)
    tail_losses = returns[returns <= var_threshold]

    return abs(tail_losses.mean())


def max_drawdown(prices):
    rolling_max = prices.cummax()
    drawdowns = (prices - rolling_max) / rolling_max

    return drawdowns.min()


def sharpe_ratio(returns, risk_free_rate=0.065):
    excess_returns = returns - (risk_free_rate / 252)

    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)


def monte_carlo_simulation(returns, n_simulations=2000, horizon=30):
    mean = returns.mean()
    std = returns.std()

    simulations = np.random.normal(
        mean,
        std,
        (n_simulations, horizon)
    )

    cumulative_returns = simulations.sum(axis=1)

    return cumulative_returns