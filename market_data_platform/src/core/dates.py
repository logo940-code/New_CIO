from datetime import datetime, date
from typing import Optional


def parse_date(value: str) -> Optional[date]:
    if not value:
        return None
    for fmt in ('%Y-%m-%d', '%d-%b-%Y', '%d/%m/%Y', '%d %B %Y', '%b %d, %Y'):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    return None
