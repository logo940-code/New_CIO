from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.services.refinancing_service import rebuild_maturity_wall


def run_pipeline() -> None:
    db: Session = SessionLocal()
    try:
        rebuild_maturity_wall(db)
    finally:
        db.close()


if __name__ == '__main__':
    run_pipeline()
