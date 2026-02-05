import pandas as pd

def write_gap_report(excel_path: str, gaps: list[dict]):
    df = pd.DataFrame([
        {
            "Gap ID": f"GAP-{str(i+1).zfill(3)}",
            "Category": g["category"],
            "Gap Description": g["description"],
            "Priority": g["priority"],
            "Suggested Article Title": g["suggested_title"],
            "Rationale": g["rationale"]
        }
        for i, g in enumerate(gaps)
    ])

    with pd.ExcelWriter(
        excel_path,
        engine="openpyxl",
        mode="a",
        if_sheet_exists="replace"
    ) as writer:
        df.to_excel(writer, sheet_name="Gap_Analysis", index=False)
