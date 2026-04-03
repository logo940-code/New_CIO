from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.repositories import get_macro_series

router = APIRouter(prefix='/macro', tags=['macro'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/series')
def series(limit: int = 500, db: Session = Depends(get_db)):
    return get_macro_series(db, None, limit)


@router.get('/series/{series_code}')
def series_code(series_code: str, limit: int = 500, db: Session = Depends(get_db)):
    return get_macro_series(db, series_code, limit)
