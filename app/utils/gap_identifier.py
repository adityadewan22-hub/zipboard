from app.utils.data_loader import load_excel
from app.utils.generation import call_gemini
from app.utils.prepare_llm_data import to_json
from app.utils.chunker import chunk_articles
from app.utils.prompt_builder import build_gap_prompt
from app.utils.deduplication import deduplicate_gaps

def identify_gaps(trimmed_data):

    all_gaps = []

    for chunk in chunk_articles(trimmed_data):

        prompt = build_gap_prompt(chunk)

        response = call_gemini(prompt)

        gaps = response.get("gaps", [])

        all_gaps.extend(gaps)

    return deduplicate_gaps(all_gaps)

