from sqlalchemy.orm import Session
from src.db.models import GOJSecurityCurated, YieldCurveSnapshot, YieldCurveNode
from src.transform.yield_curve_builder import build_curve_snapshot


def rebuild_latest_curve(db: Session):
    import pandas as pd

    rows = db.query(GOJSecurityCurated).all()
    if not rows:
        return None
    frame = pd.DataFrame([{'maturity_date': r.maturity_date, 'yield_to_maturity': r.yield_to_maturity} for r in rows])
    curve_date = max(r.as_of_date for r in rows if r.as_of_date)
    nodes = build_curve_snapshot(frame, curve_date)
    snap = YieldCurveSnapshot(curve_date=curve_date)
    db.add(snap)
    db.commit()
    db.refresh(snap)
    for _, n in nodes.iterrows():
        db.add(YieldCurveNode(snapshot_id=snap.id, tenor_years=float(n['tenor_years']), yield_value=float(n['yield_value'])))
    db.commit()
    return snap
