def build_gap_prompt(chunk):

    return f"""
You are a documentation analyst.

Analyze the following help center articles and identify documentation gaps.

Articles:
{chunk}

Return ONLY valid JSON in this format:

{{
 "gaps":[
   {{
     "gap_id":"GAP-001",
     "category":"Integrations",
     "description":"...",
     "priority":"High | Medium | Low",
     "suggested_title":"...",
     "rationale":"..."
   }}
 ]
}}

Rules:
- Do NOT hallucinate features.
- Prefer gaps that block user workflows.
- Avoid duplicates.
- Be specific.
- No markdown.
- No explanations.
"""
