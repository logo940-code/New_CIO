import pytest
pd = pytest.importorskip("pandas")
from datetime import date
from src.transform.yield_curve_builder import build_curve_snapshot


def test_curve_builder_returns_nodes():
    df = pd.DataFrame({'maturity_date': ['2027-04-01', '2029-04-01'], 'yield_to_maturity': [7.5, 8.0]})
    curve = build_curve_snapshot(df, date(2026, 4, 1))
    assert len(curve) == 2
