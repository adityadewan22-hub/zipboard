

def chunk_articles(data, size=40):
    for i in range(0, len(data), size):
        yield data[i:i+size]