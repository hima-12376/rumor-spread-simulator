import feedparser

def fetch_news(rumor):

    query = rumor.replace(" ", "+")

    url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:5]:
        articles.append(entry.title)

    return articles