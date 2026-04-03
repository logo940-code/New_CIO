from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.repositories import get_latest_curve_nodes, get_curve_history

router = APIRouter(prefix='/yield-curves', tags=['yield-curves'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/latest')
def latest(db: Session = Depends(get_db)):
    return get_latest_curve_nodes(db)


@router.get('/history')
def history(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return get_curve_history(db, start_date, end_date)
