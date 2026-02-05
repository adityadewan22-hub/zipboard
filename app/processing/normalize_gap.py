from app.utils.parse_llm import parse_llm_gap_block

def normalize_gap_outputs(llm_outputs: list[str]) -> list[dict]:
    """
    Converts raw LLM text into structured gap candidates.
    """
    # Example expected fields per gap:
    # description, category, priority, suggested_title, rationale

    # If LLM already returns JSON-like → parse
    # Else → simple regex / delimiter parsing (acceptable here)

    normalized = []
    for output in llm_outputs:
        normalized.extend(parse_llm_gap_block(output))

    return normalized
