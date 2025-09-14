#!/usr/bin/env bash
set -euo pipefail

export PYTHONUNBUFFERED=1
export DATABASE_URL=${DATABASE_URL:-postgresql+psycopg://postgres:postgres@localhost:5432/llm_tutor}
export REDIS_URL=${REDIS_URL:-redis://localhost:6379/0}
export SECRET_KEY=${SECRET_KEY:-change_me}

echo "Running backend on :8000"
cd "$(dirname "$0")/../backend" && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

