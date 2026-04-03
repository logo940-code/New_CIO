from sqlalchemy.orm import Session
from src.db.models import GOJSecurityCurated, MaturityWallSummary
from src.transform.maturity_profile_builder import build_maturity_wall


def rebuild_maturity_wall(db: Session) -> None:
    import pandas as pd

    rows = db.query(GOJSecurityCurated).all()
    if not rows:
        return
    df = pd.DataFrame([{'maturity_date': r.maturity_date, 'price': r.price or 0.0} for r in rows])
    wall = build_maturity_wall(df)
    db.query(MaturityWallSummary).delete()
    for _, r in wall.iterrows():
        db.add(MaturityWallSummary(period_start=r['period_start'].date(), period_type=r['period_type'], maturity_total=float(r['maturity_total']), liquidity_wave_score=float(r['liquidity_wave_score'])))
    db.commit()
