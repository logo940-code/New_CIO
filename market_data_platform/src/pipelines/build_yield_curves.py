from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.services.yield_curve_service import rebuild_latest_curve


def run_pipeline() -> None:
    db: Session = SessionLocal()
    try:
        rebuild_latest_curve(db)
    finally:
        db.close()


if __name__ == '__main__':
    run_pipeline()
