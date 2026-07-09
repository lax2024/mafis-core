from data.fetcher import fetch_ohlcv
from data.preprocessor import (
    add_sma,
    add_ema,
    add_rsi,
    add_macd,
    add_atr,
    add_bollinger_bands
)
from utils.signals import generate_signal


class TechnicalAgent:
    def analyze(self, ticker: str, historical_df=None):
        ticker = ticker.strip().upper()

        # Use historical slice during backtesting
        if historical_df is not None:
            df = historical_df.copy()
        else:
            df = fetch_ohlcv(ticker)

        # Add indicators
        df = add_sma(df)
        df = add_ema(df)
        df = add_rsi(df)
        df = add_macd(df)
        df = add_atr(df)
        df = add_bollinger_bands(df)

        latest = df.iloc[-1]

        signal, confidence, reasons = generate_signal(
            rsi=latest["RSI"],
            macd=latest["MACD"],
            macd_signal=latest["MACD_Signal"],
            price=latest["Close"],
            sma50=latest["SMA_50"],
            sma200=latest["SMA_200"]
        )

        # Bollinger Band override logic
        if latest["Close"] < latest["BB_Lower"]:
            signal = "BUY"
            confidence = min(confidence + 0.10, 1.0)
            reasons.append(
                "Price below lower Bollinger Band (oversold)"
            )

        elif latest["Close"] > latest["BB_Upper"]:
            signal = "SELL"
            confidence = min(confidence + 0.10, 1.0)
            reasons.append(
                "Price above upper Bollinger Band (overbought)"
            )

        return {
            "ticker": ticker,
            "signal": signal,
            "confidence": confidence,
            "price": float(latest["Close"]),
            "rsi": float(latest["RSI"]),
            "macd": float(latest["MACD"]),
            "atr": float(latest["ATR"]),
            "bb_upper": float(latest["BB_Upper"]),
            "bb_lower": float(latest["BB_Lower"]),
            "reasons": reasons
        }