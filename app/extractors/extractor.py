import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

def classify_content_type(title):
    t = title.lower()

    if t.startswith("how"):
        return "How-To Guide"
    elif "error" in t or "fix" in t or "issue" in t:
        return "Troubleshooting"
    elif t.startswith("what") or t.startswith("why"):
        return "Overview"
    elif "integration" in t:
        return "Integration Guide"
    else:
        return "General Guide"


def extract_article(url):

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find("article", id="fullArticle")

    # ---------- ARTICLE ID ----------
    article_id = url.split("/article/")[1].split("-")[0]

    # ---------- TITLE ----------
    title = article.find("h1").get_text(strip=True)

    # ---------- CATEGORY ----------
    category = None
    category_tag = soup.select_one("#sidebar .active a")

    if category_tag:
        category = category_tag.get_text(strip=True)

    # ---------- LAST UPDATED ----------
    time_tag = soup.find("time", class_="lu")

    last_updated = None
    if time_tag:
        last_updated = time_tag.get_text(strip=True).replace("Last updated on ", "")

    

    # ---------- WORD COUNT ----------
    article_text = article.get_text(" ", strip=True)
    word_count = len(article_text.split())

    # ---------- HAS SCREENSHOTS ----------
    has_screenshots = bool(article.find_all("img"))

    # ---------- CONTENT TYPE ----------
    content_type = classify_content_type(title)

    return {
        "article_id": article_id,
        "article_title": title,
        "category": category,
        "URL": url,
        "last_updated": last_updated,

    # ---- ANALYSIS FIELDS (initially empty) ----
        "content_hash": "",          # filled later
        "analysis_scope": False,     # set later
        "topics_covered": "",
        "content_type": content_type,
        "gaps_identified": "",
        "last_llm_run": "",

    # ---- METADATA ----
       "word_count": word_count,
       "has_screenshots": has_screenshots
    }
