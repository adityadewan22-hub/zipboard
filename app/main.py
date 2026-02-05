from app.orchestrator import run_full_audit
from app.config import EXCEL_PATH

if __name__ == "__main__":
    run_full_audit(EXCEL_PATH)
