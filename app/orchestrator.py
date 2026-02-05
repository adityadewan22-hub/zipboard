from app.services.run_article_audit import run_article_audit
from app.services.run_gap_synthesis import run_gap_synthesis


def run_full_audit(excel_path: str):
    run_article_audit(excel_path)   # WINS 1–4
    run_gap_synthesis(excel_path)   # WIN 5
