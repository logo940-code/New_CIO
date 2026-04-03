from datetime import datetime


def normalize_macro_workbook(sheet_frames: dict, source_url: str, series_code: str):
    import pandas as pd

    records = []
    for sheet, df in sheet_frames.items():
        df = df.copy()
        date_col = next((c for c in df.columns if 'date' in str(c).lower()), df.columns[0])
        value_cols = [c for c in df.columns if c != date_col]
        for _, row in df.iterrows():
            obs_date = pd.to_datetime(row[date_col], errors='coerce')
            if pd.isna(obs_date):
                continue
            for col in value_cols:
                val = pd.to_numeric(row[col], errors='coerce')
                if pd.isna(val):
                    continue
                records.append({
                    'series_code': f'{series_code}.{sheet}.{col}'.lower().replace(' ', '_'),
                    'observation_date': obs_date.date(),
                    'value': float(val),
                    'unit': None,
                    'source_url': source_url,
                    'ingestion_timestamp': datetime.utcnow(),
                })
    long_df = pd.DataFrame(records)
    wide_df = long_df.pivot_table(index='observation_date', columns='series_code', values='value', aggfunc='first').reset_index() if not long_df.empty else pd.DataFrame()
    return long_df, wide_df
