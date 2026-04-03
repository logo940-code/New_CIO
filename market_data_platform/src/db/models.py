from datetime import datetime, date
from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class SourceRegistry(Base):
    __tablename__ = 'source_registry'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    source_url: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class IngestionRun(Base):
    __tablename__ = 'ingestion_runs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey('source_registry.id'), index=True)
    pipeline_name: Mapped[str] = mapped_column(String(128), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default='running')


class RawFile(Base):
    __tablename__ = 'raw_files'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingestion_run_id: Mapped[int] = mapped_column(ForeignKey('ingestion_runs.id'), index=True)
    source_url: Mapped[str] = mapped_column(Text)
    file_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    local_path: Mapped[str] = mapped_column(Text)
    ingestion_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ParsingEvent(Base):
    __tablename__ = 'parsing_events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    raw_file_id: Mapped[int] = mapped_column(ForeignKey('raw_files.id'), index=True)
    parser_name: Mapped[str] = mapped_column(String(128))
    parsing_confidence: Mapped[float] = mapped_column(Float, default=1.0)
    details: Mapped[str] = mapped_column(Text, default='{}')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BOJAuctionCurated(Base):
    __tablename__ = 'boj_auctions_curated'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auction_date: Mapped[date] = mapped_column(Date, index=True)
    instrument_name: Mapped[str] = mapped_column(String(255), index=True)
    issue_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    maturity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    offer_amount: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    total_bids_received: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    total_allocated_amount: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    average_yield: Mapped[float | None] = mapped_column(Float, nullable=True)
    source_url: Mapped[str] = mapped_column(Text)
    parsing_confidence: Mapped[float] = mapped_column(Float, default=1.0)
    ingestion_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('auction_date', 'instrument_name', 'source_url', name='uq_auction_business'),)


class GOJSecurityCurated(Base):
    __tablename__ = 'goj_securities_curated'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    as_of_date: Mapped[date] = mapped_column(Date, index=True)
    security_name: Mapped[str] = mapped_column(String(255), index=True)
    isin: Mapped[str | None] = mapped_column(String(32), nullable=True)
    coupon_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    maturity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_coupon_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    previous_coupon_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    yield_to_maturity: Mapped[float | None] = mapped_column(Float, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    benchmark_bucket: Mapped[str | None] = mapped_column(String(64), nullable=True)
    instrument_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    coupon_frequency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_url: Mapped[str] = mapped_column(Text)
    parsing_confidence: Mapped[float] = mapped_column(Float, default=1.0)
    ingestion_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('as_of_date', 'security_name', 'source_url', name='uq_security_business'),)


class MacroSeriesRegistry(Base):
    __tablename__ = 'macro_series_registry'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    series_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    series_name: Mapped[str] = mapped_column(String(255))
    unit: Mapped[str | None] = mapped_column(String(64), nullable=True)


class MacroSeriesObservation(Base):
    __tablename__ = 'macro_series_observations'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    series_code: Mapped[str] = mapped_column(String(64), index=True)
    observation_date: Mapped[date] = mapped_column(Date, index=True)
    value: Mapped[float] = mapped_column(Float)
    source_url: Mapped[str] = mapped_column(Text)
    ingestion_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('series_code', 'observation_date', 'source_url', name='uq_macro_obs'),)


class YieldCurveSnapshot(Base):
    __tablename__ = 'yield_curve_snapshots'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    curve_date: Mapped[date] = mapped_column(Date, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class YieldCurveNode(Base):
    __tablename__ = 'yield_curve_nodes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    snapshot_id: Mapped[int] = mapped_column(ForeignKey('yield_curve_snapshots.id'), index=True)
    tenor_years: Mapped[float] = mapped_column(Float)
    yield_value: Mapped[float] = mapped_column(Float)
    __table_args__ = (UniqueConstraint('snapshot_id', 'tenor_years', name='uq_curve_node'),)


class MaturityWallSummary(Base):
    __tablename__ = 'maturity_wall_summary'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_start: Mapped[date] = mapped_column(Date, index=True)
    period_type: Mapped[str] = mapped_column(String(16))
    maturity_total: Mapped[float] = mapped_column(Float)
    liquidity_wave_score: Mapped[float] = mapped_column(Float)


class QCResult(Base):
    __tablename__ = 'qc_results'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    table_name: Mapped[str] = mapped_column(String(128), index=True)
    record_key: Mapped[str] = mapped_column(String(255), index=True)
    rule_name: Mapped[str] = mapped_column(String(128))
    severity: Mapped[str] = mapped_column(String(16), default='warning')
    passed: Mapped[bool] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

Index('ix_macro_series_date', MacroSeriesObservation.series_code, MacroSeriesObservation.observation_date)
