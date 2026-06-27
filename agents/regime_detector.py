from data.fetcher import fetch_ohlcv


class RegimeDetector:
    def __init__(self):
        self.short_window = 20
        self.long_window = 50

    def detect(self, ticker, historical_df=None):

        # Use historical slice if backtesting
        if historical_df is not None:
            df = historical_df.copy()
        else:
            df = fetch_ohlcv(ticker, period="6mo")

        if len(df) < self.long_window:
            return {
                "regime": "SIDEWAYS",
                "confidence": 0.5
            }

        # Moving averages
        df["SMA20"] = df["Close"].rolling(
            self.short_window
        ).mean()

        df["SMA50"] = df["Close"].rolling(
            self.long_window
        ).mean()

        sma20 = float(df["SMA20"].iloc[-1])
        sma50 = float(df["SMA50"].iloc[-1])

        # Volatility
        volatility = float(
            df["Close"].pct_change()
            .rolling(20)
            .std()
            .iloc[-1]
        )

        # Detect regime
        if sma20 > sma50:
            regime = "BULLISH"
        elif sma20 < sma50:
            regime = "BEARISH"
        else:
            regime = "SIDEWAYS"

        # Confidence
        confidence = min(
            1.0,
            abs(sma20 - sma50) / sma50
        )

        # Penalize high volatility
        if volatility > 0.04:
            confidence *= 0.8

        return {
            "regime": regime,
            "confidence": confidence,
            "sma20": sma20,
            "sma50": sma50,
            "volatility": volatility
        }