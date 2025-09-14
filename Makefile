SHELL := /bin/bash

.PHONY: help up down build backend frontend worker fmt test

help:
	@echo "Targets: up, down, build, backend, frontend, worker, fmt, test"

up:
	docker compose -f llm-tutor/infra/docker-compose.yml up -d --build

down:
	docker compose -f llm-tutor/infra/docker-compose.yml down -v

build:
	docker compose -f llm-tutor/infra/docker-compose.yml build

backend:
	cd llm-tutor/backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd llm-tutor/frontend && npm run dev

worker:
	cd llm-tutor/backend && celery -A app.workers.celery_app.celery_app worker --loglevel=INFO

fmt:
	cd llm-tutor/backend && ruff check --fix . && ruff format .
	cd llm-tutor/frontend && npx prettier --write .

test:
	cd llm-tutor/backend && pytest -q
