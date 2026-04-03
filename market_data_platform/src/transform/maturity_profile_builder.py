def build_maturity_wall(securities_df):
    import pandas as pd

    df = securities_df.copy()
    df['maturity_date'] = pd.to_datetime(df['maturity_date'])
    df = df[df['maturity_date'].notna()]
    df['period_start'] = df['maturity_date'].dt.to_period('M').dt.to_timestamp()
    agg = df.groupby('period_start', as_index=False)['price'].sum().rename(columns={'price': 'maturity_total'})
    agg['period_type'] = 'month'
    agg['liquidity_wave_score'] = agg['maturity_total'] / agg['maturity_total'].rolling(3, min_periods=1).mean()
    return agg
