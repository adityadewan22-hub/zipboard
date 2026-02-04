

def deduplicate_gaps(gaps):

    seen = set()
    unique = []

    for gap in gaps:

        key = gap["description"].lower()

        if key not in seen:
            seen.add(key)
            unique.append(gap)

    return unique
