import re
from datetime import datetime
from typing import Optional
from src.core.dates import parse_date


def infer_coupon_frequency(previous_coupon_date: Optional[str], next_coupon_date: Optional[str]) -> Optional[int]:
    prev = parse_date(previous_coupon_date) if previous_coupon_date else None
    nxt = parse_date(next_coupon_date) if next_coupon_date else None
    if not prev or not nxt:
        return None
    delta_days = (nxt - prev).days
    if delta_days <= 100:
        return 4
    if delta_days <= 190:
        return 2
    if delta_days <= 370:
        return 1
    return None


def parse_rate_sheet_row(row: dict, source_url: str, as_of_date: str | None = None) -> dict:
    coupon = row.get('coupon_rate') or row.get('coupon')
    ytm = row.get('yield_to_maturity') or row.get('ytm')
    parsed = {
        'security_name': str(row.get('security_name') or row.get('security') or '').strip(),
        'isin': row.get('isin'),
        'coupon_rate': float(str(coupon).replace('%', '').strip()) if coupon not in (None, '') else None,
        'maturity_date': parse_date(str(row.get('maturity_date') or '')),
        'next_coupon_date': parse_date(str(row.get('next_coupon_date') or '')),
        'previous_coupon_date': parse_date(str(row.get('previous_coupon_date') or '')),
        'yield_to_maturity': float(str(ytm).replace('%', '').strip()) if ytm not in (None, '') else None,
        'price': float(row['price']) if row.get('price') not in (None, '') else None,
        'benchmark_bucket': row.get('benchmark_bucket'),
        'issue_date': parse_date(str(row.get('issue_date') or '')),
        'instrument_type': row.get('instrument_type') or ('Bond' if re.search(r'bond', str(row), re.I) else None),
        'day_count_basis': row.get('day_count_basis'),
        'source_url': source_url,
        'as_of_date': parse_date(as_of_date) if as_of_date else parse_date(str(row.get('as_of_date') or '')),
        'ingestion_timestamp': datetime.utcnow(),
    }
    parsed['coupon_frequency'] = infer_coupon_frequency(
        str(row.get('previous_coupon_date') or ''), str(row.get('next_coupon_date') or '')
    )
    populated = sum(v is not None and v != '' for v in parsed.values())
    parsed['parsing_confidence'] = min(1.0, populated / 12)
    return parsed
