from datetime import date


def build_curve_snapshot(securities_df, curve_date: date):
    import pandas as pd

    df = securities_df.copy()
    df = df[df['maturity_date'].notna() & df['yield_to_maturity'].notna()]
    df['tenor_years'] = (pd.to_datetime(df['maturity_date']) - pd.to_datetime(curve_date)).dt.days / 365.25
    df = df[df['tenor_years'] > 0]
    grouped = df.groupby(df['tenor_years'].round(2), as_index=False)['yield_to_maturity'].mean()
    grouped.rename(columns={'yield_to_maturity': 'yield_value', 'tenor_years': 'tenor_years'}, inplace=True)
    return grouped.sort_values('tenor_years')
