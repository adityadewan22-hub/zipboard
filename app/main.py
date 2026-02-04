import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from app.services.fetch_article_content import fetch_article_content
from app.processing.compute_hash import compute_content_hash
from app.processing.detect_state import detect_article_state
from app.utils.build_article_prompt import build_article_analysis_prompt
from app.utils.generation import call_gemini


def run():
    df = pd.read_excel("articles.xlsx")

    for idx, row in df.iterrows():

        # 1️⃣ Scope gate
        if not row["analysis_scope"]:
            continue

        url = row["URL"]

        # 2️⃣ Fetch normalized content (WIN 2)
        text = fetch_article_content(url)

        # 3️⃣ Compute hash (WIN 3)
        new_hash = compute_content_hash(text)

        # 4️⃣ Detect state (WIN 3)
        state = detect_article_state(row["content_hash"], new_hash)

        # 5️⃣ Skip unchanged
        if state == "UNCHANGED":
            continue

        # 6️⃣ Persist hash immediately
        df.at[idx, "content_hash"] = new_hash

        # ⛔ STOP HERE for WIN 3

        prompt = build_article_analysis_prompt(
        article_text=text,
        article_title=row["article_title"],
        category=row["category"]
        )

        llm_result = call_gemini(prompt)
        df.at[idx, "topics_covered"] = ", ".join(llm_result["topics_covered"])
        df.at[idx, "content_type"] = llm_result["content_type"]
        df.at[idx, "gaps_identified"] = "; ".join(llm_result["gaps_identified"])
        df.at[idx, "last_llm_run"] = pd.Timestamp.utcnow().isoformat()
        break
        # LLM comes in WIN 4

    df.to_excel("articles.xlsx", index=False)

if __name__ == "__main__":
    run()
