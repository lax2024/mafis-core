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
 
      "STRONG BUY": 1.5,
      "BUY": 1.0,
      "HOLD": 0.0,
      "SELL": -1.0,
      "STRONG SELL": -1.5

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
                "technical": 0.50,
                "sentiment": 0.30,
                "risk": 0.20
            }

        elif regime == "BEARISH":
            return {
                "technical": 0.45,
                "sentiment": 0.35,
                "risk": 0.20
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
        if fused_score >= 0.70:
           recommendation = "STRONG BUY"

        elif fused_score >= 0.45:
            recommendation = "BUY"

        elif fused_score <= -0.70:
            recommendation = "STRONG SELL"

        elif fused_score <= -0.45:
            recommendation = "SELL"

        else:
            recommendation = "HOLD"

        
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

        # Save logs only during live analysis
        if historical_df is None:
          save_log(result)

        return result