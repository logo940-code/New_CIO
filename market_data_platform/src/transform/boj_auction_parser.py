import re
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from src.core.dates import parse_date
from src.core.hashing import sha256_bytes


@dataclass
class AuctionRecord:
    auction_date: Optional[datetime.date] = None
    instrument_name: Optional[str] = None
    issue_date: Optional[datetime.date] = None
    maturity_date: Optional[datetime.date] = None
    tenor_days: Optional[int] = None
    offer_amount: Optional[float] = None
    total_bids_received: Optional[float] = None
    total_successful_bids: Optional[float] = None
    total_allocated_bids: Optional[float] = None
    total_allocated_amount: Optional[float] = None
    average_yield: Optional[float] = None
    average_price: Optional[float] = None
    lowest_submitted_bid_rate: Optional[float] = None
    highest_submitted_bid_rate: Optional[float] = None
    highest_bid_rate_for_full_allocation: Optional[float] = None
    bid_rate_for_partial_allocation: Optional[float] = None
    partial_allocation_percentage: Optional[float] = None
    settlement_date: Optional[datetime.date] = None
    total_nominal_outstanding_on_settlement_date: Optional[float] = None
    source_url: Optional[str] = None
    source_publication_date: Optional[datetime.date] = None
    ingestion_timestamp: datetime = datetime.utcnow()
    raw_text_hash: Optional[str] = None
    parsing_confidence: float = 1.0


def _extract_float(pattern: str, text: str) -> Optional[float]:
    m = re.search(pattern, text, flags=re.IGNORECASE)
    if not m:
        return None
    candidate = m.group(1).replace(',', '')
    try:
        return float(candidate)
    except ValueError:
        return None


def _extract_date(label: str, text: str):
    m = re.search(rf"{re.escape(label)}\s*[:\-]\s*([^\n]+)", text, flags=re.IGNORECASE)
    return parse_date(m.group(1).strip()) if m else None


def parse_auction_text(text: str, source_url: str = '') -> dict:
    rec = AuctionRecord(source_url=source_url, raw_text_hash=sha256_bytes(text.encode('utf-8')))
    rec.instrument_name = '30-Day CD' if '30-day' in text.lower() else 'BOJ Auction Instrument'
    rec.auction_date = _extract_date('Auction Date', text)
    rec.issue_date = _extract_date('Issue Date', text)
    rec.maturity_date = _extract_date('Maturity Date', text)
    rec.settlement_date = _extract_date('Settlement Date', text)
    rec.source_publication_date = _extract_date('Publication Date', text)
    rec.offer_amount = _extract_float(r'Offer Amount[^0-9]*([0-9,]+\.?[0-9]*)', text)
    rec.total_bids_received = _extract_float(r'Total Bids Received[^0-9]*([0-9,]+\.?[0-9]*)', text)
    rec.total_allocated_amount = _extract_float(r'Total Allocated Amount[^0-9]*([0-9,]+\.?[0-9]*)', text)
    rec.average_yield = _extract_float(r'Average Yield[^0-9]*([0-9]+\.?[0-9]*)', text)
    rec.lowest_submitted_bid_rate = _extract_float(r'Lowest Submitted Bid Rate[^0-9]*([0-9]+\.?[0-9]*)', text)
    rec.highest_submitted_bid_rate = _extract_float(r'Highest Submitted Bid Rate[^0-9]*([0-9]+\.?[0-9]*)', text)

    if rec.issue_date and rec.maturity_date:
        rec.tenor_days = (rec.maturity_date - rec.issue_date).days

    found = sum(v is not None for k, v in asdict(rec).items() if k not in {'parsing_confidence', 'ingestion_timestamp'})
    rec.parsing_confidence = min(1.0, found / 12)
    return asdict(rec)
