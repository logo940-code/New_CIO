# Ingestion Runbook

## Standard run order
1. `make init-db`
2. `make ingest-auctions`
3. `make ingest-ratesheets`
4. `make ingest-macro`
5. `make build-curves`

## Backfill approach
- Add historical URLs in `config/sources.yaml`.
- Execute pipeline repeatedly with adjusted date ranges.
- Duplicate files are skipped by hash uniqueness.

## Troubleshooting
- Parser drift: inspect parsing_events payload and lower confidence rows.
- Date parsing issues: verify locale/day-month order in parser.
- QC failures: check `qc_results` and threshold logic in ingestion service.
