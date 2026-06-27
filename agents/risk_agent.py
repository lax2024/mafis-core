from data.fetcher import fetch_ohlcv
from agents.risk_metrics import *
import numpy as np


class RiskAgent:
    def analyze(self, ticker, historical_df=None):
        ticker = ticker.strip().upper()

        # Use historical slice during backtesting
        if historical_df is not None:
            df = historical_df.copy()
        else:
            df = fetch_ohlcv(ticker)

        prices = df["Close"]

        returns = log_returns(prices)

        var_95 = historical_var(returns)
        cvar_95 = cvar(returns)
        drawdown = max_drawdown(prices)
        sharpe = sharpe_ratio(returns)

        mc_results = monte_carlo_simulation(returns)

        prob_loss = (mc_results < 0).mean()

        # Composite risk score
        risk_score = (
            (abs(var_95) * 100) +
            (abs(drawdown) * 100) +
            (prob_loss * 100)
        ) / 3

        if risk_score < 15:
            risk_label = "LOW"
        elif risk_score < 30:
            risk_label = "MODERATE"
        elif risk_score < 50:
            risk_label = "HIGH"
        else:
            risk_label = "EXTREME"

        return {
            "ticker": ticker,
            "var_95": float(var_95),
            "cvar_95": float(cvar_95),
            "max_drawdown": float(drawdown),
            "sharpe_ratio": float(sharpe),
            "prob_loss_30d": float(prob_loss),
            "risk_score": float(risk_score),
            "risk_label": risk_label
        }