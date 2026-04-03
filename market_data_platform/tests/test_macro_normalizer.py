import pytest
pd = pytest.importorskip("pandas")
from src.transform.macro_series_normalizer import normalize_macro_workbook


def test_macro_normalization_long_wide():
    sheets = {'S1': pd.DataFrame({'Date': ['2026-01-31'], 'Inflation': [5.1]})}
    long_df, wide_df = normalize_macro_workbook(sheets, 'x', 'inflation')
    assert len(long_df) == 1
    assert not wide_df.empty
