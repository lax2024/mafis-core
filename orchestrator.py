from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.risk_agent import RiskAgent
from agents.regime_detector import RegimeDetector
from utils.logger import save_log


class Orchestrator:
    def __init__(self):
        self.technical = TechnicalAgent()
        self.sentiment = SentimentAgent()
        self.risk = RiskAgent()
        self.regime_detector = RegimeDetector()

    # Technical normalization
    def normalize_technical(self, signal):
        return {
            "BUY": 1.0,
            "HOLD": 0.0,
            "SELL": -1.0
        }.get(signal, 0.0)

    # Sentiment normalization
    def normalize_sentiment(self, score):
        boosted = score * 2
        return max(-1.0, min(1.0, boosted))

    # Better balanced risk normalization
    def normalize_risk(self, risk_score):
        normalized = (50 - risk_score) / 50
        return max(-1.0, min(1.0, normalized))

    # Dynamic weights
    def dynamic_weights(self, regime):
        if regime == "BULLISH":
            return {
                "technical": 0.40,
                "sentiment": 0.35,
                "risk": 0.25
            }

        elif regime == "BEARISH":
            return {
                "technical": 0.35,
                "sentiment": 0.40,
                "risk": 0.25
            }

        # SIDEWAYS
        return {
            "technical": 0.35,
            "sentiment": 0.45,
            "risk": 0.20
        }

    def analyze(self, ticker, historical_df=None):

        # Regime detection
        regime_data = self.regime_detector.detect(
            ticker,
            historical_df=historical_df
        )

        # Technical analysis
        tech = self.technical.analyze(
            ticker,
            historical_df=historical_df
        )

        # Sentiment analysis
        sent = self.sentiment.analyze(
            ticker,
            historical_date=historical_df.index[-1]
            if historical_df is not None else None
        )

        # Risk analysis
        risk = self.risk.analyze(
            ticker,
            historical_df=historical_df
        )

        # Dynamic weights
        weights = self.dynamic_weights(
            regime_data["regime"]
        )

        # Normalize scores
        tech_score = self.normalize_technical(
            tech["signal"]
        )

        sent_score = self.normalize_sentiment(
            sent["score"]
        )

        risk_score = self.normalize_risk(
            risk["risk_score"]
        )

        # Fuse scores
        fused_score = (
            tech_score * weights["technical"] +
            sent_score * weights["sentiment"] +
            risk_score * weights["risk"]
        )

        confidence = round(abs(fused_score), 3)

        # Explainability reasoning
        reasoning = []

        if tech_score > 0:
            reasoning.append("Technical trend bullish")
        elif tech_score < 0:
            reasoning.append("Technical trend bearish")
        else:
            reasoning.append("Technical trend neutral")

        if sent_score > 0.15:
            reasoning.append("Market sentiment positive")
        elif sent_score < -0.15:
            reasoning.append("Market sentiment negative")
        else:
            reasoning.append("Market sentiment neutral")

        if risk_score < 0:
            reasoning.append("Risk is elevated")
        else:
            reasoning.append("Risk is manageable")

        reasoning.append(
            f"Market regime detected as {regime_data['regime']}"
        )

        # Balanced thresholds
        if fused_score >= 0.30:
            recommendation = "BUY"

        elif fused_score <= -0.30:
            recommendation = "SELL"

        else:
            recommendation = "HOLD"

        # Debug logs
        print({
            "technical_score": tech_score,
            "sentiment_score": sent_score,
            "risk_score": risk_score,
            "weights": weights,
            "fused_score": fused_score,
            "confidence": confidence,
            "reasoning": reasoning
        })

        result = {
            "ticker": ticker,
            "recommendation": recommendation,
            "confidence": confidence,
            "fused_score": float(fused_score),
            "regime": regime_data,
            "weights_used": weights,
            "reasoning": reasoning,
            "technical": tech,
            "sentiment": sent,
            "risk": risk
        }

        save_log(result)

        return result