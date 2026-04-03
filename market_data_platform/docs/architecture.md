# Architecture

## High-level flow
1. Connector discovers candidate source assets.
2. Extractors download bytes and persist to raw layer.
3. Parsers transform source text/tables into normalized staging records.
4. Validation framework applies explicit domain QC checks.
5. Curated loaders upsert validated records into PostgreSQL.
6. Services publish downstream views for API/dashboard.

## Design characteristics
- Idempotent by file hash and business-key upserts.
- Auditability through ingestion_runs, raw_files, parsing_events, qc_results.
- Separation of concerns: connector, extract, transform, validate, load.
- Config-driven source management via `config/sources.yaml`.
