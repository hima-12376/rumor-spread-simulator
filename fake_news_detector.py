from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from news_scraper import fetch_news

def check_fake_news(rumor):

    articles = fetch_news(rumor)

    if not articles:
        return "⚠️ No Related News Found Online"

    corpus = [rumor] + articles

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    similarity = cosine_similarity(vectors[0:1], vectors[1:]).mean()

    debunk_words = [
        "fake", "myth", "false", "hoax", "misleading",
        "debunk", "rumor", "no evidence", "not true"
    ]

    for headline in articles:
        for word in debunk_words:
            if word in headline.lower():
                return "❌ Likely Fake News (Debunked Online)"

    if similarity > 0.2:
        return "✅ Likely Real News (Reported Online)"
    else:
        return "❌ Likely Fake News (No Trusted Reporting)"