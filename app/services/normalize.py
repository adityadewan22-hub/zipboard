import re

def normalize_text(text: str) -> str:
    """
    Normalizes text to make hashing and comparison stable.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()
