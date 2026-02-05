from app.utils.chunker import chunk_gap_inputs
from app.processing.deduplication import deduplicate_and_rank
from app.io.gap_sheet_maker import write_gap_report
from app.utils.synthesize_gaps import synthesize_gaps
from app.utils.read_eligible import load_gap_inputs


def run_gap_synthesis(excel_path: str):
    records = load_gap_inputs(excel_path)
    if not records:
        return

    raw= synthesize_gaps(records=records)
    raw_gaps=raw["gaps"]
    final_gaps = deduplicate_and_rank(raw_gaps)

    write_gap_report(excel_path, final_gaps)
