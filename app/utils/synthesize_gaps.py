from app.llm.generation import call_gemini
from app.llm.prompt_builder import build_gap_prompt

def synthesize_gaps(records):
    """
    records: list of dicts with keys
      - category
      - article_title
      - gaps (semicolon-separated string)
    """

    # 1. Convert article-level gaps into atomic gap candidates
    gap_candidates = []

    for r in records:
        for gap in r["gaps"].split(";"):
            gap = gap.strip()
            if not gap:
                continue

            gap_candidates.append({
                "category": r["category"],
                "description": gap,
                "source_article": r["article_title"]
            })
    print("gaps found")
    # 2. Ask LLM to synthesize (dedupe + rank)
    prompt = build_gap_prompt(gap_candidates)
    response = call_gemini(prompt)
    print("RAW GAP SYNTHESIS RESPONSE:", response)


    # 3. Expect final ranked gaps
    return response
