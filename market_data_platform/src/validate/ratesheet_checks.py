from .rules import QCCheck, check_date_order, check_non_negative


def validate_ratesheet_record(record: dict) -> list[QCCheck]:
    checks = [
        check_date_order(record.get('issue_date'), record.get('maturity_date')),
        check_non_negative('coupon_rate', record.get('coupon_rate')),
    ]
    return checks
