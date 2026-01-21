import feedparser

CRYPTO_RSS_URL = "https://cointelegraph.com/rss"


def get_latest_news(limit: int = 5) -> list[str]:
    feed = feedparser.parse(CRYPTO_RSS_URL)

    news = []
    for entry in feed.entries[:limit]:
        title = entry.title.strip()
        link = entry.link.strip()
        news.append(f"• {title}\n{link}")

    return news
