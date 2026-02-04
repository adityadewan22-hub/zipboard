def build_article_analysis_prompt(article_text, article_title, category):
    return f"""
You are a SaaS documentation analyst.

Analyze the following help article.

Title: {article_title}
Category: {category}

Article Content:
\"\"\"{article_text}\"\"\"

Return ONLY valid JSON in this format:

{{
  "topics_covered": ["topic1", "topic2", "topic3"],
  "content_type": "How-To Guide | Overview | Troubleshooting | Integration Guide | General Guide",
  "gaps_identified": [
    "Missing troubleshooting steps for failed sync",
    "No permissions matrix for non-admin users"
  ]
}}

Rules:
- Topics must reflect what the article ACTUALLY covers.
- Gaps must be based only on missing or weak info in THIS article.
- Do NOT invent features or integrations.
- Be concise.
- No markdown.
- No explanations.
"""
