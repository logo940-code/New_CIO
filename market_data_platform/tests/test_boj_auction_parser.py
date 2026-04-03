from src.transform.boj_auction_parser import parse_auction_text


def test_parse_boj_auction_text_core_fields():
    text = """Auction Date: 2026-03-10
Issue Date: 2026-03-11
Maturity Date: 2026-04-10
Offer Amount: 1,000,000
Average Yield: 8.10"""
    rec = parse_auction_text(text)
    assert rec['auction_date'].isoformat() == '2026-03-10'
    assert rec['tenor_days'] == 30
    assert rec['average_yield'] == 8.10
