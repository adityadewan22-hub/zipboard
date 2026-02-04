import hashlib

def compute_content_hash(text: str) -> str:
    """
    Computes a deterministic hash for normalized article text.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
