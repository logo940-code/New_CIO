PYTHON=python

init-db:
	$(PYTHON) -m src.db.schema_init

ingest-auctions:
	$(PYTHON) -m src.pipelines.ingest_boj_auctions

ingest-ratesheets:
	$(PYTHON) -m src.pipelines.ingest_goj_rate_sheets

ingest-macro:
	$(PYTHON) -m src.pipelines.ingest_boj_macro

build-curves:
	$(PYTHON) -m src.pipelines.build_yield_curves

run-api:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard:
	streamlit run src/dashboard/app.py

run-tests:
	pytest
