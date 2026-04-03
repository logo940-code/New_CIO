from sqlalchemy.orm import Session
from src.db.repositories import get_latest_auctions, get_latest_curve_nodes, get_maturity_wall


def dashboard_snapshot(db: Session) -> dict:
    return {
        'auctions': get_latest_auctions(db, limit=5),
        'curve_nodes': get_latest_curve_nodes(db),
        'maturity_wall': get_maturity_wall(db),
    }
