from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import BOJAuctionCurated, GOJSecurityCurated, YieldCurveSnapshot, YieldCurveNode, MacroSeriesObservation, MaturityWallSummary


def get_latest_auctions(db: Session, limit: int = 20):
    return db.scalars(select(BOJAuctionCurated).order_by(BOJAuctionCurated.auction_date.desc()).limit(limit)).all()


def get_auction_history(db: Session, start_date=None, end_date=None):
    stmt = select(BOJAuctionCurated)
    if start_date:
        stmt = stmt.where(BOJAuctionCurated.auction_date >= start_date)
    if end_date:
        stmt = stmt.where(BOJAuctionCurated.auction_date <= end_date)
    return db.scalars(stmt.order_by(BOJAuctionCurated.auction_date)).all()


def get_latest_securities(db: Session, limit: int = 50):
    return db.scalars(select(GOJSecurityCurated).order_by(GOJSecurityCurated.as_of_date.desc()).limit(limit)).all()


def get_latest_curve_nodes(db: Session):
    snap = db.scalars(select(YieldCurveSnapshot).order_by(YieldCurveSnapshot.curve_date.desc()).limit(1)).first()
    if not snap:
        return []
    return db.scalars(select(YieldCurveNode).where(YieldCurveNode.snapshot_id == snap.id).order_by(YieldCurveNode.tenor_years)).all()


def get_curve_history(db: Session, start_date=None, end_date=None):
    stmt = select(YieldCurveSnapshot)
    if start_date:
        stmt = stmt.where(YieldCurveSnapshot.curve_date >= start_date)
    if end_date:
        stmt = stmt.where(YieldCurveSnapshot.curve_date <= end_date)
    return db.scalars(stmt.order_by(YieldCurveSnapshot.curve_date)).all()


def get_macro_series(db: Session, series_code: str | None = None, limit: int = 500):
    stmt = select(MacroSeriesObservation)
    if series_code:
        stmt = stmt.where(MacroSeriesObservation.series_code == series_code)
    return db.scalars(stmt.order_by(MacroSeriesObservation.observation_date.desc()).limit(limit)).all()


def get_maturity_wall(db: Session):
    return db.scalars(select(MaturityWallSummary).order_by(MaturityWallSummary.period_start)).all()
