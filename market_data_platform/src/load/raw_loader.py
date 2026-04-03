from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.models import RawFile


def persist_raw_file(db: Session, ingestion_run_id: int, source_url: str, file_hash: str, local_path: str) -> RawFile:
    existing = db.scalar(select(RawFile).where(RawFile.file_hash == file_hash))
    if existing:
        return existing
    rf = RawFile(
        ingestion_run_id=ingestion_run_id,
        source_url=source_url,
        file_hash=file_hash,
        local_path=local_path,
        ingestion_timestamp=datetime.utcnow(),
    )
    db.add(rf)
    db.commit()
    db.refresh(rf)
    return rf
