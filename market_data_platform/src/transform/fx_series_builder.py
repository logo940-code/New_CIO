def latest_fx_snapshot(macro_long_df):
    fx = macro_long_df[macro_long_df['series_code'].str.contains('fx', case=False, na=False)].copy()
    if fx.empty:
        return fx
    latest_date = fx['observation_date'].max()
    return fx[fx['observation_date'] == latest_date]
