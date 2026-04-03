# Onboarding

1. Install Python 3.11 and Docker.
2. Copy `.env.example` to `.env` and update DB URL.
3. Install dependencies: `pip install -r requirements.txt`.
4. Start Postgres: `docker compose up -d db`.
5. Initialize schema and run pipelines.
6. Validate API health at `/health`.
