from app.utils.generation import call_gemini
from app.utils.prompt_builder import build_gap_prompt
from app.utils.deduplication import deduplicate_gaps
import pandas as pd

def generate_gap_report(df):
    scoped = df[df["analysis_scope"] == True]

    gap_inputs = []
    for _, row in scoped.iterrows():
        gap_inputs.append({
            "article_title": row["article_title"],
            "category": row["category"],
            "gaps": row["gaps_identified"]
        })

    chunks = chunk(gap_inputs)

    all_gap_rows = []
    for chunk in chunks:
        prompt = build_gap_prompt(chunk)
        result = call_gemini(prompt)
        all_gap_rows.extend(result["gaps"])

    deduped = deduplicate_gaps(all_gap_rows)
    top_5 = deduped[:5]

    return pd.DataFrame(top_5)
