from app.pipelines.run_gap_synthesis import run_gap_synthesis
from app.config import EXCEL_PATH

def main():
    print("Running gap synthesis test...")
    run_gap_synthesis(EXCEL_PATH)
    print("Gap synthesis completed.")

if __name__ == "__main__":
    main()
