Architecture Overview

- Backend: FastAPI, async SQLAlchemy, JWT auth, Celery for async jobs, SSE for streaming tutor responses.
- Data: PostgreSQL with JSONB for flexible fields; pgvector planned. Models align with spec.
- Services: RAG, Tutor Orchestrator, Quiz & Grader, Code Runner (stubbed), Math Solver (stubbed).
- Frontend: React + Vite + Tailwind + shadcn/ui; distinct 3-pane layout.
- Infra: Dockerfiles, docker-compose for local dev; GitHub Actions CI.

See API.md for endpoint details and RAG.md for retrieval design.

