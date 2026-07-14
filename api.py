import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from orchestrator import Orchestrator


app = FastAPI(
    title="MAFIS API",
    description="Multi-Agent Financial Intelligence System",
    version="1.0.0"
)

technical_agent = TechnicalAgent()
sentiment_agent = SentimentAgent()
risk_agent = RiskAgent()
orchestrator = Orchestrator()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to MAFIS API",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "running",
        "service": "MAFIS API"
    }


@app.get("/analyze/technical/{ticker}")
def analyze_technical(ticker: str):
    try:
        return technical_agent.analyze(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyze/sentiment/{ticker}")
def analyze_sentiment(ticker: str):
    try:
        return sentiment_agent.analyze(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyze/risk/{ticker}")
def analyze_risk(ticker: str):
    try:
        return risk_agent.analyze(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):
    try:
        return orchestrator.analyze(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
def get_logs():
    try:
        with open("logs/trade_logs.json", "r") as f:
            return json.load(f)

    except FileNotFoundError:
        return {
            "message": "No trade logs found yet."
        }

    except json.JSONDecodeError:
        return {
            "message": "Trade log file is corrupted.",
            "logs": []
        }