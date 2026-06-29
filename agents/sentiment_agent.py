print("NEW SENTIMENT LOGIC LOADED")

import random
from transformers import pipeline
from data.news_fetcher import fetch_news


class SentimentAgent:
    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
             model="/content/mafis-core/models/finbert_custom"

        )

        self.label_map = {
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "NEUTRAL",
            "LABEL_2": "POSITIVE"
        }

    def _mock_headlines(self, ticker):
        bullish = [
            f"{ticker} beats earnings expectations",
            f"{ticker} expands into new markets",
            f"{ticker} gains investor confidence"
        ]

        bearish = [
            f"{ticker} misses revenue estimates",
            f"{ticker} faces regulatory pressure",
            f"{ticker} stock declines amid uncertainty"
        ]

        neutral = [
            f"{ticker} trades within normal range",
            f"{ticker} market activity remains stable",
            f"{ticker} analysts maintain outlook"
        ]

        mood = random.choice(["bullish", "bearish", "neutral"])

        if mood == "bullish":
            return random.sample(bullish, 2) + [random.choice(neutral)]

        elif mood == "bearish":
            return random.sample(bearish, 2) + [random.choice(neutral)]

        else:
            return random.sample(neutral, 2) + [random.choice(bullish)]

    def _score_headlines(self, headlines):
        results = self.model(
            headlines,
            truncation=True,
            max_length=512
        )

        score = 0.0
        breakdown = []

        for headline, r in zip(headlines, results):
            raw_label = r["label"]
            confidence = r["score"]

            label = self.label_map.get(
                raw_label,
                raw_label
            ).upper()

            if label == "POSITIVE":
                score += confidence

            elif label == "NEGATIVE":
                score -= confidence

            breakdown.append({
                "headline": headline,
                "label": label,
                "confidence": round(confidence, 4)
            })

        score = score / len(results)

        final_label = (
            "POSITIVE" if score > 0
            else "NEGATIVE" if score < 0
            else "NEUTRAL"
        )

        return {
            "score": float(score),
            "label": final_label,
            "breakdown": breakdown
        }

    def analyze(self, ticker, historical_date=None):
        ticker = ticker.strip().upper()
        source = "live"

        try:
            # Historical mode
            if historical_date is not None:
                headlines = fetch_news(
                    ticker,
                    historical_date=historical_date
                )
                source = "historical"

            # Live mode
            else:
                headlines = fetch_news(ticker)

            # Fallback
            if not headlines:
                headlines = self._mock_headlines(ticker)
                source = "mock"

            scored = self._score_headlines(headlines)

            return {
                "score": scored["score"],
                "label": scored["label"],
                "headlines": headlines,
                "source": source,
                "breakdown": scored["breakdown"]
            }

        except Exception as e:
            print("[SentimentAgent Error]", e)

            return {
                "score": 0.0,
                "label": "NEUTRAL",
                "headlines": [],
                "source": "error",
                "breakdown": []
            }