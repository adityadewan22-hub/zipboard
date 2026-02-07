import time
import random
import pandas as pd
from dotenv import load_dotenv
from requests.exceptions import HTTPError

from app.extractors.fetch_article_content import fetch_article_content
from app.processing.compute_hash import compute_content_hash
from app.processing.detect_state import detect_article_state
from app.llm.build_article_prompt import build_article_analysis_prompt
from app.llm.generation import call_gemini

load_dotenv()


def run_article_audit(excel_path: str):
    df = pd.read_excel(excel_path)

    # Defensive normalization (state hygiene)
    for col in ["content_hash", "topics_covered", "gaps_identified", "last_llm_run"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    MAX_ARTICLES_PER_RUN = 50   # safety cap for CI
    processed = 0

    print(f"[Audit] Starting article audit for {len(df)} articles")

    for idx, row in df.iterrows():

        if processed >= MAX_ARTICLES_PER_RUN:
            print("[Audit] Reached per-run processing limit, stopping early")
            break

        # 1️⃣ Scope gate (manual control)
        if not row["analysis_scope"]:
            continue

        url = row["URL"]

        # 2️⃣ Fetch normalized content (with rate-limit handling)
        try:
            text = fetch_article_content(url)
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                print(f"[Audit] Rate limited on {url}, skipping for now")
                continue
            raise

        # 3️⃣ Compute hash
        new_hash = compute_content_hash(text)

        # 4️⃣ Detect state
        state = detect_article_state(row["content_hash"], new_hash)

        # 5️⃣ Skip unchanged
        if state == "UNCHANGED":
            continue

        # 6️⃣ Persist hash immediately (state correctness)
        df.at[idx, "content_hash"] = new_hash

        # 7️⃣ LLM analysis
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

        processed += 1

        # Polite throttling between requests
        time.sleep(random.uniform(2.0, 4.0))

    # Persist once, after all rows
    df.to_excel(excel_path, index=False)

    print(f"[Audit] Completed. Processed {processed} articles this run.")
