def chunk_gap_inputs(records, max_chars=6000):
    chunks, current, size = [], [], 0

    for r in records:
        block = f"""
Category: {r['category']}
Article: {r['article_title']}
Gaps:
{r['gaps']}
"""
        if size + len(block) > max_chars:
            chunks.append("\n".join(current))
            current, size = [], 0

        current.append(block)
        size += len(block)

    if current:
        chunks.append("\n".join(current))

    return chunks
