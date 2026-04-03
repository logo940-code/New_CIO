from src.transform.goj_rate_sheet_parser import parse_rate_sheet_row, infer_coupon_frequency


def test_coupon_frequency_inference_semi_annual():
    assert infer_coupon_frequency('2026-01-15', '2026-07-15') == 2


def test_parse_ratesheet_row():
    row = {
        'security_name': 'GOJ 8 2029',
        'coupon_rate': '8.0%',
        'maturity_date': '2029-07-15',
        'next_coupon_date': '2026-07-15',
        'previous_coupon_date': '2026-01-15',
        'yield_to_maturity': '7.8%',
        'price': '101.5',
        'as_of_date': '2026-04-01',
    }
    rec = parse_rate_sheet_row(row, source_url='x')
    assert rec['coupon_rate'] == 8.0
    assert rec['coupon_frequency'] == 2
