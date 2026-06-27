
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





import requests

API_KEY = "aabae42161324de381925fb57478056e"

COMPANY_MAP = {
    "AAPL": ["Apple", "AAPL"],
    "TSLA": ["Tesla", "TSLA"],
    "MSFT": ["Microsoft", "MSFT"],
    "GOOGL": ["Google", "Alphabet", "GOOGL"],
    "AMZN": ["Amazon", "AMZN"],
    "META": ["Meta", "Facebook", "META"],
    "NVDA": ["Nvidia", "NVDA"]
}


def fetch_news(ticker):
    keywords = COMPANY_MAP.get(ticker.upper(), [ticker])

    # Use only main company name for API search
    query = keywords[0]

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&language=en&sortBy=publishedAt&pageSize=15&apiKey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])

    headlines = []

    for article in articles:
        title = article.get("title", "")

        # Soft filter
        if any(keyword.lower() in title.lower() for keyword in keywords):
            headlines.append(title)

    # fallback if filter removes everything
    if len(headlines) == 0:
        headlines = [
            article.get("title", "")
            for article in articles[:10]
        ]

    return headlines