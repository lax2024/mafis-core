import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator import Orchestrator
from data.fetcher import fetch_ohlcv


class Backtester:
    def __init__(self, ticker="TSLA", capital=10000):
        self.ticker = ticker
        self.capital = capital
        self.orchestrator = Orchestrator()

    def run(self):
        df = fetch_ohlcv(self.ticker, period="1y")

        cash = self.capital
        shares = 0
        trades = []

        equity_curve = []

        for i in range(60, len(df) - 1):
            historical_df = df.iloc[:i]

            result = self.orchestrator.analyze(
                self.ticker,
                historical_df=historical_df
            )

            signal = result["recommendation"]
            current_price = float(df.iloc[i]["Close"])

            # BUY
            if signal == "BUY" and cash > 0:
                shares = cash / current_price
                cash = 0

                trades.append({
                    "type": "BUY",
                    "date": df.index[i],
                    "price": current_price
                })

            # SELL
            elif signal == "SELL" and shares > 0:
                cash = shares * current_price
                shares = 0

                trades.append({
                    "type": "SELL",
                    "date": df.index[i],
                    "price": current_price
                })

            portfolio_value = cash + (shares * current_price)
            equity_curve.append(portfolio_value)

        final_price = float(df.iloc[-1]["Close"])
        final_value = cash + (shares * final_price)

        total_return = (
            (final_value - self.capital) / self.capital
        ) * 100

        # ===== PERFORMANCE METRICS =====

        profits = []
        buy_price = None

        for trade in trades:
            if trade["type"] == "BUY":
                buy_price = trade["price"]

            elif trade["type"] == "SELL" and buy_price is not None:
                profit = trade["price"] - buy_price
                profits.append(profit)

        total_trades = len(profits)

        winning_trades = len(
            [p for p in profits if p > 0]
        )

        losing_trades = len(
            [p for p in profits if p <= 0]
        )

        win_rate = (
            (winning_trades / total_trades) * 100
            if total_trades > 0 else 0
        )

        avg_profit = (
            sum(profits) / total_trades
            if total_trades > 0 else 0
        )

        peak = max(equity_curve)
        trough = min(equity_curve)

        max_drawdown = (
            ((peak - trough) / peak) * 100
            if peak > 0 else 0
        )

        # Plot equity curve
        plt.figure(figsize=(12, 6))
        plt.plot(equity_curve)
        plt.title(f"{self.ticker} Equity Curve")
        plt.xlabel("Trading Steps")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.show()

        return {
            "ticker": self.ticker,
            "initial_capital": self.capital,
            "final_value": round(final_value, 2),
            "total_return_percent": round(total_return, 2),
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 2),
            "average_profit_per_trade": round(avg_profit, 2),
            "max_drawdown_percent": round(max_drawdown, 2),
            "trades": trades
        }


if __name__ == "__main__":
    bt = Backtester("TSLA")
    result = bt.run()
    print(result)