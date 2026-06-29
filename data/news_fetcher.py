
# import requests

# API_KEY = "aabae42161324de381925fb57478056e"


# def fetch_news(query):
#     url = (
#         f"https://newsapi.org/v2/everything?"
#         f"q={query}&language=en&sortBy=publishedAt&pageSize=10&apiKey={API_KEY}"
#     )

#     response = requests.get(url)
#     data = response.json()

#     articles = data.get("articles", [])

#     headlines = []

#     for article in articles:
#         title = article.get("title", "")

#         if query.split()[0].upper() in title.upper():
#             headlines.append(title)

#     return headlines





import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(ticker, historical_date=None):
    try:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={ticker}&language=en&sortBy=publishedAt"
            f"&apiKey={API_KEY}"
        )

        if historical_date:
            date_str = str(historical_date).split(" ")[0]
            url += f"&from={date_str}&to={date_str}"

        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])

        headlines = [
            article["title"]
            for article in articles[:5]
            if article.get("title")
        ]

        return headlines

    except Exception as e:
        print("[NewsFetcher Error]", e)
        return []