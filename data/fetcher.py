import yfinance as yf
import pandas as pd
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

INDIAN_STOCKS = {
    "TCS",
    "RELIANCE",
    "INFY",
    "HDFCBANK",
    "ICICIBANK"
}


def fetch_ohlcv(
    ticker: str,
    period: str = "5y",
    interval: str = "1d",
    force_refresh: bool = False,
) -> pd.DataFrame:

    ticker = ticker.upper()

    # Convert Indian stocks to NSE format
    if ticker in INDIAN_STOCKS:
        ticker = f"{ticker}.NS"

    cache_path = CACHE_DIR / f"{ticker}_{period}_{interval}.parquet"

    # Load cached data
    if cache_path.exists() and not force_refresh:
        df = pd.read_parquet(cache_path)
        print(f"[Fetcher] Loaded {ticker} from cache")
        return df

    # Download fresh data
    print(f"[Fetcher] Downloading {ticker}...")

    raw = yf.download(
        ticker,
        period=period,
        interval=interval,
        progress=False
    )

    if raw.empty:
        raise ValueError(f"No data found for {ticker}")

    # Flatten multi-index if needed
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    # Keep required OHLCV columns
    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()

    # Normalize datetime index
    df.index = pd.to_datetime(df.index).tz_localize(None)

    # Remove null rows
    df.dropna(inplace=True)

    # Save to cache
    df.to_parquet(cache_path)

    return df