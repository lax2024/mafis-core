import matplotlib.pyplot as plt
import time
import sys
from pathlib import Path

Path("plots").mkdir(exist_ok=True)

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
        buy_hold_curve = []

        buy_hold_shares = self.capital / float(df.iloc[60]["Close"])

        for i in range(60, len(df) - 1):
            historical_df = df.iloc[:i]

            result = self.orchestrator.analyze(
                self.ticker,
                historical_df=historical_df
            )

            signal = result["recommendation"]
            current_price = float(df.iloc[i]["Close"])

            # BUY (50% allocation)
            if signal == "BUY" and cash > 0:

              investment = cash * 0.50

              shares += investment / current_price
              cash -= investment

              trades.append({
                "type": "BUY",
                "date": df.index[i],
                "price": current_price
              })

            #STRONG BUY (100% allocation)
            elif signal == "STRONG BUY" and cash > 0:

             investment = cash

             shares += investment / current_price
             cash = 0

             trades.append({
               "type": "STRONG BUY",
                "date": df.index[i],
              "price": current_price
             })

            # SELL (sell 50%)
            elif signal == "SELL" and shares > 0:

             sell_shares = shares * 0.50

             cash += sell_shares * current_price
             shares -= sell_shares

             trades.append({
              "type": "SELL",
              "date": df.index[i],
              "price": current_price
             })

            # STRONG SELL (sell everything)
            elif signal == "STRONG SELL" and shares > 0:

             cash += shares * current_price
             shares = 0

             trades.append({
               "type": "STRONG SELL",
                "date": df.index[i],
               "price": current_price
             })

            portfolio_value = cash + (shares * current_price)
            equity_curve.append(portfolio_value)

            buy_hold_value = buy_hold_shares * current_price
            buy_hold_curve.append(buy_hold_value)

        final_price = float(df.iloc[-1]["Close"])
        final_value = cash + (shares * final_price)

        strategy_return = (
            (final_value - self.capital) / self.capital
        ) * 100

        buy_hold_final = buy_hold_shares * final_price
        buy_hold_return = (
            (buy_hold_final - self.capital) / self.capital
        ) * 100

        alpha = strategy_return - buy_hold_return


        beat_buy_and_hold = strategy_return > buy_hold_return



        # Profit analysis
        profits = []
        buy_price = None

        for trade in trades:
            if trade["type"] in ["BUY", "STRONG BUY"]:
             buy_price = trade["price"]

            elif trade["type"] in ["SELL", "STRONG SELL"] and buy_price is not None:
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

        # Max drawdown
        running_peak = equity_curve[0]
        drawdowns = []

        for value in equity_curve:
            running_peak = max(running_peak, value)
            drawdown = (
                (running_peak - value) / running_peak
            ) * 100
            drawdowns.append(drawdown)

        max_drawdown = max(drawdowns)

        # Sharpe ratio
        returns = []

        for i in range(1, len(equity_curve)):
            r = (
                equity_curve[i] - equity_curve[i - 1]
            ) / equity_curve[i - 1]
            returns.append(r)

        avg_return = (
            sum(returns) / len(returns)
            if returns else 0
        )

        volatility = (
            (
                sum(
                    (r - avg_return) ** 2
                    for r in returns
                ) / len(returns)
            ) ** 0.5
            if returns else 0
        )

        sharpe_ratio = (
            (avg_return / volatility) * (252 ** 0.5)
            if volatility > 0 else 0
        )

        # Plot comparison
        plt.figure(figsize=(14, 7))
        plt.plot(equity_curve, label="MAFIS Strategy")
        plt.plot(buy_hold_curve, label="Buy & Hold")
        plt.title(
            f"{self.ticker} Strategy vs Buy-and-Hold"
        )
        plt.xlabel("Trading Steps")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.grid(True)
        plt.savefig(
         f"plots/{self.ticker}_backtest.png",
         dpi=300,
         bbox_inches="tight"
        )
        plt.close()

        return {
            "ticker": self.ticker,
            "initial_capital": self.capital,
            "final_value": round(final_value, 2),
            "strategy_return_percent": round(
                strategy_return, 2
            ),
            "buy_hold_return_percent": round(
                buy_hold_return, 2
            ),
            "alpha_percent": round(alpha, 2),
            "beat_buy_and_hold": beat_buy_and_hold,
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 2),
            "average_profit_per_trade": round(
                avg_profit, 2
            ),
            "max_drawdown_percent": round(
                max_drawdown, 2
            ),
            "sharpe_ratio": round(
                sharpe_ratio, 2
            ),
            "trades": trades
        }


if __name__ == "__main__":
    tickers = [
    "TSLA",
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "RELIANCE",
    "TCS",
    "INFY"
]

    start = time.time()

    all_results = []

    for ticker in tickers:
     print(f"\nRunning backtest for {ticker}...\n")

     try:
        bt = Backtester(ticker)
        result = bt.run()

        print(
         f"{ticker}: "
         f"Return={result['strategy_return_percent']}%, "
         f"Alpha={result['alpha_percent']}%, "
         f"Sharpe={result['sharpe_ratio']}"
        )


        all_results.append({
            "ticker": ticker,
            "strategy_return": result["strategy_return_percent"],
            "buy_hold_return": result["buy_hold_return_percent"],
            "alpha": result["alpha_percent"],
            "sharpe": result["sharpe_ratio"],

            "win_rate": result["win_rate"],
            "beat_buy_and_hold": result["beat_buy_and_hold"]


        })

     except Exception as e:
        print(f"{ticker} failed: {e}")

    print("\n===== FINAL SUMMARY =====")

    for r in all_results:

      print(
        f"{r['ticker']:10}"
        f" Return={r['strategy_return']:7.2f}%"
        f" Alpha={r['alpha']:7.2f}%"
        f" Sharpe={r['sharpe']:6.2f}"
        f" WinRate={r['win_rate']:6.2f}%"
        f" BeatBH={r['beat_buy_and_hold']}"
      )

        


    if all_results:
     avg_alpha = sum(
        r["alpha"] for r in all_results
     ) / len(all_results)

     avg_sharpe = sum(
        r["sharpe"] for r in all_results
     ) / len(all_results)

     avg_winrate = sum(
        r["win_rate"] for r in all_results
     ) / len(all_results)

     print("\n===== AVERAGES =====")
     print("Average Alpha:", round(avg_alpha, 2))
     print("Average Sharpe:", round(avg_sharpe, 2))
     print("Average Win Rate:", round(avg_winrate, 2))
    else:
     print("No successful backtests.")

    print(
    "\nExecution Time:",
    round(time.time() - start, 2),
    "seconds"
    )