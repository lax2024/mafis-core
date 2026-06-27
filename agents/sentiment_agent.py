print("NEW SENTIMENT LOGIC LOADED")

from transformers import pipeline
import random


class SentimentAgent:
    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model="./models/finbert_custom"
        )

        self.label_map = {
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "NEUTRAL",
            "LABEL_2": "POSITIVE"
        }

    def generate_mock_headlines(self, ticker):
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
            return random.sample(bullish, 2) + [
                random.choice(neutral)
            ]

        elif mood == "bearish":
            return random.sample(bearish, 2) + [
                random.choice(neutral)
            ]

        else:
            return random.sample(neutral, 2) + [
                random.choice(bullish)
            ]

    def analyze(self, ticker, historical_date=None):
        try:
            # Ignore old cached historical files completely
            headlines = self.generate_mock_headlines(ticker)

            print(f"[Sentiment] Headlines: {headlines}")

            results = self.model(headlines)

            print(f"[Sentiment] Raw model output: {results}")

            score = 0.0

            for r in results:
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

            score = score / len(results)

            final_label = (
                "POSITIVE" if score > 0
                else "NEGATIVE" if score < 0
                else "NEUTRAL"
            )

            return {
                "score": float(score),
                "label": final_label,
                "headlines": headlines
            }

        except Exception as e:
            print("[SentimentAgent Error]", e)

            return {
                "score": 0.0,
                "label": "NEUTRAL",
                "headlines": []
            }