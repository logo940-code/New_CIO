import pandas as pd
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.models import MacroSeriesObservation
from src.services.ingestion_service import start_ingestion_run, complete_run
from src.transform.macro_series_normalizer import normalize_macro_workbook
from src.load.curated_loader import upsert_rows


def run_pipeline() -> None:
    db: Session = SessionLocal()
    run = start_ingestion_run(db, 'boj_macro', 'config', 'ingest_boj_macro')
    try:
        sample = {'Sheet1': pd.DataFrame({'Date': ['2026-01-31', '2026-02-28'], 'FX Purchases': [10, 12]})}
        long_df, _ = normalize_macro_workbook(sample, 'internal://sample/boj-macro', 'fx_flows')
        upsert_rows(db, MacroSeriesObservation, long_df.to_dict(orient='records'), ['series_code', 'observation_date', 'source_url'])
        complete_run(db, run)
    except Exception:
        complete_run(db, run, status='failed')
        raise
    finally:
        db.close()


if __name__ == '__main__':
    run_pipeline()
