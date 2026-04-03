from datetime import date
from .rules import QCCheck, check_non_negative, check_not_future


def validate_auction(record: dict, as_of: date) -> list[QCCheck]:
    checks = [
        check_non_negative('average_yield', record.get('average_yield')),
        check_not_future('auction_date', record.get('auction_date'), as_of),
    ]
    return checks
