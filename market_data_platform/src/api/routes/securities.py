from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.repositories import get_latest_securities

router = APIRouter(prefix='/securities', tags=['securities'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/latest')
def latest(limit: int = 50, db: Session = Depends(get_db)):
    return get_latest_securities(db, limit)
