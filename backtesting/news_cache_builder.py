import os
import json
import yfinance as yf


def build_news_cache(ticker="TSLA"):
    print(f"Building historical news cache for {ticker}...")

    # Download 1 year stock data
    data = yf.download(ticker, period="1y")

    # Create cache folder
    os.makedirs("./cache/news", exist_ok=True)

    for date in data.index:
        date_str = str(date.date())

        # Dummy historical headlines (acts as your backtest dataset)
        headlines = [
            f"{ticker} stock moves sharply on {date_str}",
            f"{ticker} investor sentiment shifts after price action",
            f"{ticker} analysts react to market volatility"
        ]

        filename = f"./cache/news/{ticker}_{date_str}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {"headlines": headlines},
                f,
                indent=4
            )

        print(f"Saved: {filename}")


if __name__ == "__main__":
    build_news_cache("TSLA")