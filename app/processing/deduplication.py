def deduplicate_and_rank(gaps: list[dict], top_n=5):
    seen = {}
    for gap in gaps:
        key = gap["description"].lower().strip()
        if key not in seen:
            seen[key] = gap

    ranked = sorted(
        seen.values(),
        key=lambda g: {"High": 0, "Medium": 1, "Low": 2}[g["priority"]]
    )

    return ranked[:top_n]
