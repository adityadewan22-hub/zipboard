import pandas as pd
import json
from app.utils.data_loader import load_excel
#THIS FILE CONVERTS THE SHEET DATA INTO JSON FOR LLM TO REASON ON

df=load_excel("zipboard_help_articles.xlsx")

def to_json(df):
    articles = df.to_dict(orient="records")

    trimmed = [
        {
            "title": a["article_title"],
            "category": a["category"],
            "topics": a["topics_covered"],
            "word_count": a["word_count"],
            "content_type": a["content_type"]
        }
        for a in articles
    ]

    return trimmed


