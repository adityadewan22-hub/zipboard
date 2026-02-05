import pandas as pd

def load_gap_inputs(excel_path: str) -> list[dict]:
    df = pd.read_excel(excel_path)

    eligible = df[
        (df["analysis_scope"] == True) &
        (df["gaps_identified"].notna()) &
        (df["gaps_identified"].str.strip() != "")
    ]

    records = []
    for _, row in eligible.iterrows():
        records.append({
            "category": row["category"],
            "article_title": row["article_title"],
            "gaps": row["gaps_identified"]
        })

    return records
