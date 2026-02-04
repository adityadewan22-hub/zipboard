from app.services.fetch_article_content import fetch_article_content
from app.processing.compute_hash import compute_content_hash
from app.processing.detect_state import detect_article_state

TEST_URL = "https://help.zipboard.co/article/63-how-do-i-integrate-zipboard-with-jira"

test_row = {
    "URL": TEST_URL,
    "content_hash": "",      # simulate first run
    "analysis_scope": True
}

# ---- FIRST RUN ----
text = fetch_article_content(TEST_URL)
new_hash = compute_content_hash(text)

state = detect_article_state(test_row["content_hash"], new_hash)
print("STATE (first run):", state)

# ✅ Simulate persisting hash (THIS WAS MISSING)
test_row["content_hash"] = new_hash


# ---- SECOND RUN ----
text = fetch_article_content(TEST_URL)
new_hash_2 = compute_content_hash(text)

state_2 = detect_article_state(test_row["content_hash"], new_hash_2)
print("STATE (second run):", state_2)

text = fetch_article_content(TEST_URL)
text = text + " dummy change for testing"

new_hash_3 = compute_content_hash(text)
state = detect_article_state(test_row["content_hash"], new_hash_3)

print("STATE:", state)