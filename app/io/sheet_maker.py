import json
import pandas as pd
import time
from tqdm import tqdm
from app.services.extractor import extract_article

# ✅ Load URLs discovered earlier
with open("article_urls.json", "r") as f:
    article_urls = json.load(f)

articles = []

for url in tqdm(article_urls):
    try:
        article = extract_article(url)
        articles.append(article)

        time.sleep(0.4)  # polite scraping

    except Exception as e:
        print(f"Failed for {url}: {e}")

# ✅ Create dataframe
df = pd.DataFrame(articles)

# OPTIONAL but HIGHLY recommended
df["topics_covered"] = df["topics_covered"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else ""
)

# ✅ Export
df.to_excel("zipboard_help_articles.xlsx", index=False)

print("Spreadsheet created successfully ✅")
