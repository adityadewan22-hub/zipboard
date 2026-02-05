import requests
from bs4 import BeautifulSoup
import json
from app.extractors.extractor import extract_article

sitemap_url = "https://help.zipboard.co/sitemap.xml"

response = requests.get(sitemap_url)
soup = BeautifulSoup(response.text, "xml")  
# IMPORTANT: use "xml", not html.parser

urls = [loc.text for loc in soup.find_all("loc")]

article_urls = [u for u in urls if "/article/" in u]

with open("article_urls.json", "w") as f:
    json.dump(article_urls, f, indent=2)
print(f"Collected {len(article_urls)} article URLs")

