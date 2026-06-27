from fastapi import FastAPI
from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from orchestrator import Orchestrator
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException




app = FastAPI()

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
    return {"message": "MAFIS API Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/analyze/technical/{ticker}")
def analyze_technical(ticker: str):
    result = technical_agent.analyze(ticker)
    return result

@app.get("/analyze/sentiment/{ticker}")
def analyze_sentiment(ticker: str):
    result = sentiment_agent.analyze(ticker)
    return result

@app.get("/analyze/risk/{ticker}")
def analyze_risk(ticker: str):
    result = risk_agent.analyze(ticker)
    return result

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):
    try:
        return orchestrator.analyze(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
def get_logs():
    with open("logs/trade_logs.json", "r") as f:
        return json.load(f)
    
@app.get("/health")
def health():
    return {"status": "running"}