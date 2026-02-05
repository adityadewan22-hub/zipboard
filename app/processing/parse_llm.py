import re

def parse_llm_gap_block(text: str) -> list[dict]:
    gaps = []

    # Split on "Gap:" or numbered gaps
    blocks = re.split(r"\n\s*(?:Gap\s*\d*:|Gap:)", text)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        def extract(label):
            match = re.search(
                rf"{label}\s*:\s*(.+?)(?=\n[A-Z][a-zA-Z ]+?:|\Z)",
                block,
                re.DOTALL
            )
            return match.group(1).strip() if match else ""

        gap = {
            "category": extract("Category"),
            "description": extract("Description"),
            "priority": extract("Priority"),
            "suggested_title": extract("Suggested Article"),
            "rationale": extract("Rationale")
        }

        # Hard validation — discard garbage
        if gap["description"] and gap["priority"]:
            gaps.append(gap)

    return gaps
