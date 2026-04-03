from datetime import date, datetime
from sqlalchemy.orm import Session
from src.db.models import IngestionRun, SourceRegistry, ParsingEvent, QCResult
from src.load.curated_loader import upsert_rows


def start_ingestion_run(db: Session, source_code: str, source_url: str, pipeline_name: str) -> IngestionRun:
    source = db.query(SourceRegistry).filter_by(source_code=source_code).first()
    if not source:
        source = SourceRegistry(source_code=source_code, source_url=source_url)
        db.add(source)
        db.commit()
        db.refresh(source)
    run = IngestionRun(source_id=source.id, pipeline_name=pipeline_name)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def complete_run(db: Session, run: IngestionRun, status: str = 'completed') -> None:
    run.status = status
    run.completed_at = datetime.utcnow()
    db.add(run)
    db.commit()


def persist_qc_results(db: Session, table_name: str, record_key: str, checks) -> bool:
    all_pass = True
    for check in checks:
        qc = QCResult(
            table_name=table_name,
            record_key=record_key,
            rule_name=check.rule_name,
            severity=check.severity,
            passed=1 if check.passed else 0,
            message=check.message,
        )
        if not check.passed and check.severity in {'error'}:
            all_pass = False
        db.add(qc)
    db.commit()
    return all_pass


def record_parsing_event(db: Session, raw_file_id: int, parser_name: str, confidence: float, details: str = '{}') -> None:
    event = ParsingEvent(raw_file_id=raw_file_id, parser_name=parser_name, parsing_confidence=confidence, details=details)
    db.add(event)
    db.commit()
