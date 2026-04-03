# Caribbean Market Data Platform (Internal)

Production-minded internal platform for Jamaica and regional treasury/market intelligence.

## What this MVP includes
- 3-layer data architecture: raw, staging, curated.
- Resilient parser modules for BOJ auctions, GOJ rate sheets, and BOJ macro XLS/XLSX.
- PostgreSQL schema and SQLAlchemy models with lineage tables.
- Validation/QC framework with persisted QC results.
- FastAPI service for internal data consumers.
- Streamlit dashboard starter with CIO-focused pages.
- Pipeline scripts for ingestion, curve building, and refinancing summaries.

## Quickstart
1. `cp .env.example .env`
2. `pip install -r requirements.txt`
3. `docker compose up -d db`
4. `make init-db`
5. `make ingest-auctions && make ingest-ratesheets && make ingest-macro`
6. `make build-curves`
7. `make run-api`
8. `make run-dashboard`

## Core layers
- **Raw**: source bytes, hash, and source metadata persisted unchanged.
- **Staging**: parsed and normalized records with parse confidence.
- **Curated**: QC-evaluated analyst-grade tables for APIs and dashboards.

## Backfills
All pipelines are idempotent through file-hash uniqueness and upsert keys. Run with historical source configs and date filters.

## Tests
`make run-tests`
