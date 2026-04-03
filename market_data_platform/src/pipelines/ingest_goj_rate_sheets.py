from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.models import GOJSecurityCurated
from src.services.ingestion_service import start_ingestion_run, complete_run, persist_qc_results
from src.transform.goj_rate_sheet_parser import parse_rate_sheet_row
from src.validate.ratesheet_checks import validate_ratesheet_record
from src.load.curated_loader import upsert_rows


def run_pipeline() -> None:
    db: Session = SessionLocal()
    run = start_ingestion_run(db, 'goj_rate_sheets', 'config', 'ingest_goj_rate_sheets')
    try:
        sample_row = {
            'security_name': 'JMD GLOBAL BOND 8.00 2029',
            'coupon_rate': '8.0',
            'maturity_date': '2029-07-15',
            'next_coupon_date': '2026-07-15',
            'previous_coupon_date': '2026-01-15',
            'yield_to_maturity': '7.85',
            'price': 101.2,
            'as_of_date': '2026-04-01',
            'instrument_type': 'Bond',
        }
        rec = parse_rate_sheet_row(sample_row, source_url='internal://sample/goj-ratesheet')
        checks = validate_ratesheet_record(rec)
        allowed = persist_qc_results(db, 'goj_securities_curated', f"{rec.get('as_of_date')}|{rec.get('security_name')}", checks)
        if allowed:
            upsert_rows(db, GOJSecurityCurated, [rec], ['as_of_date', 'security_name', 'source_url'])
        complete_run(db, run)
    except Exception:
        complete_run(db, run, status='failed')
        raise
    finally:
        db.close()


if __name__ == '__main__':
    run_pipeline()
