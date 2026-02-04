def detect_article_state(stored_hash: str, new_hash: str) -> str:
    """
    Determines whether an article is NEW, UPDATED, or UNCHANGED.
    """
    if not stored_hash:
        return "NEW"

    if stored_hash != new_hash:
        return "UPDATED"

    return "UNCHANGED"
