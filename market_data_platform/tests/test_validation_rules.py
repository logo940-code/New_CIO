from datetime import date
from src.validate.rules import check_date_order, check_non_negative, check_not_future


def test_check_date_order_fails_when_reversed():
    res = check_date_order(date(2026, 4, 10), date(2026, 4, 1))
    assert not res.passed


def test_non_negative():
    assert not check_non_negative('coupon_rate', -1).passed


def test_not_future_warning():
    assert not check_not_future('auction_date', date(2099, 1, 1), date(2026, 4, 3)).passed
