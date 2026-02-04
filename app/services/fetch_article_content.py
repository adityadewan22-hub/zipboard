import requests
from bs4 import BeautifulSoup
from app.services.normalize import normalize_text

headers = {"User-Agent": "Mozilla/5.0"}

def fetch_article_content(url: str) -> str:
    """
    Fetches and returns the cleaned main article text
    from a zipBoard help article URL.
    """

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    article = soup.find("article", id="fullArticle")
    if not article:
        raise ValueError(f"No article content found for {url}")

    # Extract readable text only
    raw_text = article.get_text(separator=" ", strip=True)
    normalized_text=normalize_text(raw_text)

    return normalized_text


