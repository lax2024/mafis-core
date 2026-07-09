# MAFIS — Multi-Agent Financial Intelligence System

**A multi-agent AI platform for stock market analysis, combining technical indicators, FinBERT-based sentiment analysis, quantitative risk metrics, and market regime detection into a single fused investment recommendation.**

Final Year Project — Master of Computer Applications (MCA)
St. Joseph’s College Devagiri, Kozhikode

-----

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [API Endpoints](#api-endpoints)
- [Backtesting & Evaluation](#backtesting--evaluation)
- [FinBERT Model Training & Evaluation](#finbert-model-training--evaluation)
- [Environment Variables](#environment-variables)
- [Future Scope](#future-scope)

-----

## Overview

Most stock analysis tools rely on a single signal — either price action or news sentiment — which leads to false signals and poor risk-awareness. MAFIS addresses this by running four independent agents in parallel and **fusing** their outputs with regime-aware dynamic weighting, rather than trusting any single indicator in isolation.

|Agent              |Responsibility                                |Output                                  |
|-------------------|----------------------------------------------|----------------------------------------|
|**Technical Agent**|RSI, MACD, SMA, Golden/Death Cross            |`BUY` / `HOLD` / `SELL`                 |
|**Sentiment Agent**|Fine-tuned FinBERT on financial news headlines|Sentiment score + label                 |
|**Risk Agent**     |VaR, CVaR, Sharpe Ratio, Max Drawdown         |Risk label (`Low` / `Moderate` / `High`)|
|**Regime Detector**|SMA20 vs SMA50 trend classification           |`BULLISH` / `BEARISH` / `SIDEWAYS`      |

The **Orchestrator** combines all four outputs using **regime-dependent weighted fusion** and produces a final recommendation along with a human-readable explanation of *why* — addressing the explainability gap in typical black-box trading signals.

-----

## Architecture

```
                         ┌─────────────────────────┐
                         │   User Input (Ticker)    │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────▼─────────────┐
                         │   Frontend (Next.js)      │
                         │   mafis-dashboard/         │
                         └────────────┬─────────────┘
                                      │ REST (JSON)
                         ┌────────────▼─────────────┐
                         │   FastAPI Backend          │
                         │   api.py                   │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────▼─────────────┐
                         │   Orchestrator Engine      │
                         │   orchestrator.py          │
                         └────────────┬─────────────┘
                                      │
        ┌───────────────┬────────────┼────────────┬───────────────┐
        ▼                ▼            ▼            ▼               
┌───────────────┐ ┌─────────────┐ ┌──────────┐ ┌─────────────────┐
│ Technical Agent│ │ Sentiment   │ │ Risk     │ │ Regime Detector │
│ (RSI/MACD/SMA) │ │ Agent       │ │ Agent    │ │ (SMA20 vs SMA50)│
│                │ │ (FinBERT)   │ │ (VaR/    │ │                 │
│                │ │             │ │ Sharpe)  │ │                 │
└───────┬────────┘ └──────┬──────┘ └────┬─────┘ └────────┬────────┘
        │                 │             │                │
        └─────────────────┴──────┬──────┴────────────────┘
                                  ▼
                     ┌─────────────────────────┐
                     │   Fusion Engine           │
                     │   (dynamic regime-based   │
                     │   weighted scoring)        │
                     └────────────┬─────────────┘
                                  ▼
                     ┌─────────────────────────┐
                     │ Strong Buy / Buy / Hold /  │
                     │ Sell / Strong Sell          │
                     │  + confidence + reasoning   │
                     └────────────┬─────────────┘
                                  ▼
                     ┌─────────────────────────┐
                     │   Logging (logs.json)     │
                     │   + Visualization          │
                     └─────────────────────────┘
```

**Data flow for backtesting** is identical, except the Orchestrator is fed a rolling historical slice of OHLCV data day-by-day (with a 60-day warmup window) instead of live data, and the Sentiment Agent pulls headlines from a date-filtered historical news CSV instead of the live NewsAPI — keeping the backtest leakage-free.

-----

## Project Structure

```
mafis-core/
├── api.py                          # FastAPI app — all REST endpoints
├── orchestrator.py                 # Fusion engine: combines agent outputs
├── requirements.txt
├── .env.example                    # Template for backend environment variables
│
├── agents/
│   ├── technical_agent.py          # RSI, MACD, SMA, crossover signals
│   ├── sentiment_agent.py          # FinBERT inference (live + historical)
│   ├── risk_agent.py               # Aggregates risk metrics -> risk label
│   ├── risk_metrics.py             # VaR, CVaR, Sharpe Ratio, Drawdown math
│   └── regime_detector.py          # Bullish/Bearish/Sideways classification
│
├── data/
│   ├── fetcher.py                  # yFinance OHLCV fetch + Parquet caching
│   ├── news_fetcher.py             # Live NewsAPI integration (cached)
│   ├── historical_news.py          # Ticker+date filtered historical headlines
│   ├── preprocessor.py             # Indicator calculations (SMA/EMA/RSI/MACD/ATR)
│   ├── raw_news.csv                # Raw labelled financial news corpus
│   ├── news_dataset.csv            # Cleaned dataset used for FinBERT fine-tuning
│   └── cache/                      # Cached OHLCV Parquet files (gitignored)
│
├── training/
│   ├── prepare_dataset.py          # Cleans raw_news.csv -> news_dataset.csv
│   ├── finetune_finbert.py         # Fine-tunes ProsusAI/finbert
│   ├── evaluate_model.py           # Held-out test evaluation + metrics export
│   └── sanity_check.py             # Quick manual inspection of dataset rows
│
├── backtesting/
│   ├── orchestrator_backtester.py  # Single-ticker MAFIS backtest + equity curve
│   ├── strategy_comparison.py      # MAFIS vs Buy & Hold vs RSI-only, CSV export
│   └── news_cache_builder.py       # Pre-builds historical news cache
│
├── utils/
│   ├── logger.py                   # Appends every /analyze result to logs.json
│   └── signals.py                  # Shared signal/label helpers
│
├── models/
│   └── finbert_custom/             # Fine-tuned FinBERT weights + tokenizer
│
├── logs.json                       # Append-only log of all analysis results
│
└── mafis-dashboard/
    └── mafis-dashboard/            # Next.js + TypeScript frontend
        ├── app/                    # App Router pages
        ├── components/dashboard/   # Recommendation, Risk, Sentiment, Regime cards etc.
        ├── components/ui/          # shadcn/ui primitives
        ├── lib/api.ts              # Typed fetch client for the FastAPI backend
        └── lib/types.ts            # Shared TypeScript types matching API responses
```

-----

## Tech Stack

|Layer      |Technology                                                                |
|-----------|--------------------------------------------------------------------------|
|Backend API|Python, FastAPI, Uvicorn                                                  |
|ML / NLP   |PyTorch, HuggingFace Transformers, fine-tuned FinBERT (`ProsusAI/finbert`)|
|Data       |yFinance, Pandas, NumPy, Parquet (caching)                                |
|Frontend   |Next.js (App Router), React, TypeScript, Tailwind CSS, shadcn/ui, Recharts|
|Evaluation |scikit-learn (precision/recall/F1, confusion matrix), Matplotlib          |

-----

## Backend Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/lax2024/mafis-core.git
cd mafis-core

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install python-dotenv scikit-learn matplotlib   # required for .env loading + evaluation script

# 4. Configure environment variables
cp .env.example .env
# Open .env and add your NewsAPI key:
#   NEWS_API_KEY=your_newsapi_key_here

# 5. Run the FastAPI server
uvicorn api:app --reload
```

The API will be available at **`http://127.0.0.1:8000`**, with interactive Swagger docs at **`http://127.0.0.1:8000/docs`**.

> **Note:** the first request to any `/analyze*` endpoint will be slower than subsequent ones, since the fine-tuned FinBERT model is loaded into memory on startup.

-----

## Frontend Setup

### Prerequisites

- Node.js 18+
- npm

### Installation

```bash
cd mafis-dashboard/mafis-dashboard

# 1. Install dependencies
npm install

# 2. Configure environment variables
cp .env.local.example .env.local
# Defaults to:
#   NEXT_PUBLIC_MAFIS_API_URL=http://127.0.0.1:8000

# 3. Run the development server
npm run dev
```

The dashboard will be available at **`http://localhost:3000`**. Make sure the FastAPI backend (`uvicorn api:app --reload`) is running first, since the frontend fetches all analysis data from it.

**Available scripts:**

|Command        |Purpose                                 |
|---------------|----------------------------------------|
|`npm run dev`  |Start development server with hot reload|
|`npm run build`|Production build                        |
|`npm run start`|Run the production build                |
|`npm run lint` |Lint the codebase                       |

-----

## API Endpoints

Base URL: `http://127.0.0.1:8000`

|Method|Endpoint                     |Description                                                                                         |
|------|-----------------------------|----------------------------------------------------------------------------------------------------|
|`GET` |`/`                          |Health check / welcome message                                                                      |
|`GET` |`/health`                    |Service health status                                                                               |
|`GET` |`/analyze/{ticker}`          |**Full MAFIS analysis** — runs all agents, fuses scores, returns final recommendation with reasoning|
|`GET` |`/analyze/technical/{ticker}`|Technical Agent only (RSI, MACD, SMA signals)                                                       |
|`GET` |`/analyze/sentiment/{ticker}`|Sentiment Agent only (FinBERT score on live news)                                                   |
|`GET` |`/analyze/risk/{ticker}`     |Risk Agent only (VaR, CVaR, Sharpe, Drawdown, risk label)                                           |
|`GET` |`/analyze/regime/{ticker}`   |Regime Detector only (Bullish/Bearish/Sideways)                                                     |
|`GET` |`/logs?limit=100`            |Returns the most recent analysis results logged to `logs.json`                                      |

### Example: full analysis

```bash
curl http://127.0.0.1:8000/analyze/AAPL
```

```json
{
  "ticker": "AAPL",
  "recommendation": "BUY",
  "confidence": 0.412,
  "fused_score": 0.412,
  "regime": { "regime": "BULLISH", "confidence": 0.78 },
  "weights_used": { "technical": 0.40, "sentiment": 0.35, "risk": 0.25 },
  "reasoning": [
    "Technical trend bullish",
    "Market sentiment positive",
    "Risk is manageable",
    "Market regime detected as BULLISH"
  ],
  "technical": { "signal": "BUY", "..." : "..." },
  "sentiment": { "score": 0.31, "label": "POSITIVE", "source": "live", "..." : "..." },
  "risk": { "risk_score": 28, "risk_label": "Moderate", "..." : "..." }
}
```

Indian (NSE-listed) tickers are also supported (e.g. `TCS`, `RELIANCE`, `INFY`, `HDFCBANK`, `ICICIBANK`) — the `.NS` suffix is appended automatically by `data/fetcher.py`.

-----

## Backtesting & Evaluation

### Single-ticker MAFIS backtest

Runs the full Orchestrator day-by-day over historical data and plots an equity curve:

```bash
python backtesting/orchestrator_backtester.py
```

Reports total return, win rate, average profit per trade, and max drawdown.

### Strategy comparison (MAFIS vs Buy & Hold vs RSI-only)

Benchmarks MAFIS against a passive Buy & Hold strategy and a single-indicator RSI-only baseline, across multiple tickers, and exports results to CSV:

```bash
python backtesting/strategy_comparison.py
python backtesting/strategy_comparison.py --tickers AAPL,TSLA,TCS,INFY --period 2y
python backtesting/strategy_comparison.py --capital 50000 --output backtesting/results/comparison.csv
```

Output CSV columns: `ticker, strategy, initial_capital, final_value, total_return_pct, sharpe_ratio, max_drawdown_pct, win_rate_pct, total_trades`

All three strategies trade over the same warmup-adjusted time window, so results are directly comparable — and a console summary table (averaged across all tickers) is printed at the end for quick reporting.

-----

## FinBERT Model Training & Evaluation

### 1. Prepare the dataset

```bash
python training/prepare_dataset.py
```

Cleans `data/raw_news.csv` (headline + label) and saves `data/news_dataset.csv`.

### 2. Fine-tune FinBERT

```bash
python training/finetune_finbert.py
```

Fine-tunes `ProsusAI/finbert` on the first 5,000 rows of `news_dataset.csv` (85/15 stratified train/validation split), and saves the best checkpoint to `models/finbert_custom/`.

### 3. Evaluate on a held-out test set

```bash
python training/evaluate_model.py
```

Automatically builds a genuine held-out test set from the rows of `news_dataset.csv` **never seen during training or validation** (everything beyond the first 5,000 rows), then reports:

- Accuracy, macro/weighted Precision, Recall, F1
- Full per-class classification report
- Confusion matrix (printed + saved as `training/eval_results/confusion_matrix.png`)
- Complete results saved to `training/eval_results/classification_report.json`

-----

## Environment Variables

**Backend** (`.env` at repo root — copy from `.env.example`):

|Variable      |Description                                                                      |
|--------------|---------------------------------------------------------------------------------|
|`NEWS_API_KEY`|API key for [NewsAPI.org](https://newsapi.org), used for live sentiment headlines|

**Frontend** (`mafis-dashboard/mafis-dashboard/.env.local` — copy from `.env.local.example`):

|Variable                   |Description                                                       |
|---------------------------|------------------------------------------------------------------|
|`NEXT_PUBLIC_MAFIS_API_URL`|Base URL of the FastAPI backend (default: `http://127.0.0.1:8000`)|


> `.env` files are gitignored and should never be committed.

-----

## Future Scope

- Portfolio-level analysis across multiple tickers with allocation suggestions
- Reinforcement learning for dynamic agent weight tuning
- Cryptocurrency market support
- Real-time alerting (regime change / strong signal notifications)
- Cloud deployment (Docker + CI/CD)
- HMM-based regime detection (currently SMA20/SMA50 crossover-based)

-----

## Author

**Lakshmi Nanda K**
Master of Computer Applications
St. Joseph’s College Devagiri, Kozhikode
