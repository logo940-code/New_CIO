from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.repositories import get_macro_series

router = APIRouter(prefix='/fx', tags=['fx'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/latest')
def latest(db: Session = Depends(get_db)):
    rows = get_macro_series(db, limit=1000)
    fx = [r for r in rows if 'fx' in r.series_code.lower()]
    return fx[:50]
