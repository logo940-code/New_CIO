from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.db.repositories import get_maturity_wall

router = APIRouter(tags=['refinancing'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/refinancing/windows')
def windows(db: Session = Depends(get_db)):
    return get_maturity_wall(db)


@router.get('/maturity-wall')
def maturity_wall(db: Session = Depends(get_db)):
    return get_maturity_wall(db)
