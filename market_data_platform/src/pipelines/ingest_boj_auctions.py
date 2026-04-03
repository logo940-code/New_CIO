from datetime import date
from sqlalchemy.orm import Session
from config.settings import get_settings
from src.db.session import SessionLocal
from src.db.models import BOJAuctionCurated
from src.services.ingestion_service import start_ingestion_run, complete_run, persist_qc_results
from src.transform.boj_auction_parser import parse_auction_text
from src.validate.auction_checks import validate_auction
from src.load.curated_loader import upsert_rows


def run_pipeline() -> None:
    settings = get_settings()
    db: Session = SessionLocal()
    run = start_ingestion_run(db, 'boj_auctions', 'config', 'ingest_boj_auctions')
    try:
        sample_text = 'Auction Date: 2026-03-10
Issue Date: 2026-03-11
Maturity Date: 2026-04-10
Offer Amount: 5000000000
Average Yield: 8.25
Total Bids Received: 6200000000
Total Allocated Amount: 5000000000'
        rec = parse_auction_text(sample_text, source_url='internal://sample/boj-auction')
        checks = validate_auction(rec, date.today())
        allowed = persist_qc_results(db, 'boj_auctions_curated', f"{rec.get('auction_date')}|{rec.get('instrument_name')}", checks)
        if allowed:
            upsert_rows(db, BOJAuctionCurated, [rec], ['auction_date', 'instrument_name', 'source_url'])
        complete_run(db, run)
    except Exception:
        complete_run(db, run, status='failed')
        raise
    finally:
        db.close()


if __name__ == '__main__':
    run_pipeline()
