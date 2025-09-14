LLM Tutor Platform — MVP

An LLM‑powered STEM tutoring platform that lets learners study structured course content, chat with an AI tutor that cites sources, generate and grade practice, and track progress. The codebase is designed for reliability, testability, performance, and fast iteration.

Quick links
- docs: `llm-tutor/docs/ARCHITECTURE.md`, `llm-tutor/docs/API.md`, `llm-tutor/docs/RAG.md`, `llm-tutor/docs/SECURITY.md`
- backend entry: `llm-tutor/backend/app/main.py`
- frontend entry: `llm-tutor/frontend/src/main.tsx`
- compose: `llm-tutor/infra/docker-compose.yml`

Features
- Users & Auth: Email/password login, JWT access token + httpOnly refresh cookie; roles: student, admin.
- Content: Course → Module → Lesson hierarchy; lessons in Markdown; document upload (PDF/MD) with automatic chunking and embeddings.
- Tutor Chat: Streaming SSE responses; architecture supports tools (RAG search, quiz gen/grade, math, code runner).
- Practice & Assessment: Quiz generate/grade stubs with structured outputs for UI; rubric/feedback placeholders.
- Progress: Track lesson completion and basic analytics endpoints.
- Admin: Upload documents, trigger reindex; CRUD scaffolding ready to extend.
- Observability: Optional Sentry and OpenTelemetry hooks; simple rate limiting middleware.

Tech Stack
- Backend: FastAPI (async), Python 3.11, SQLAlchemy 2.x async, PostgreSQL + pgvector, Alembic (scaffold), Celery + Redis, SSE (sse-starlette)
- Frontend: React + TypeScript + Vite, TailwindCSS, Zustand, React Router, Framer Motion (ready)
- CI/Infra: Docker + Compose; GitHub Actions (lint, test, build)

Repository Layout

```
llm-tutor/
  backend/
    app/
      api/            routers (auth, catalog, documents, rag, chat, tools, progress, admin)
      core/           settings, deps, security
      db/             models, session
      services/       rag, tutor, embeddings, chunking, ingest
      utils/          observability, rate limit, paths
      workers/        celery tasks
      main.py         FastAPI app
    tests/            pytest tests
    alembic/          migrations scaffold
    pyproject.toml
  frontend/
    src/
      components/     FileDrop, CitationsPanel
      pages/          App, Login, Register, Courses, Lesson, Chat, Practice, Admin
      lib/            api fetchers
      store/          auth store
      main.tsx        router
    index.html
    package.json
    vite.config.ts
    tailwind.config.js
  infra/
    docker/
      backend.Dockerfile
      frontend.Dockerfile
      worker.Dockerfile
    docker-compose.yml
    k8s/ (scaffold)
  scripts/
    dev.sh
    seed.py
  docs/
    ARCHITECTURE.md · API.md · RAG.md · SECURITY.md
  .github/workflows/ci.yml
  .env.example
  Makefile
```

Use Cases
- Learn a lesson: Browse courses, open a lesson, read Markdown content with math/code blocks, then continue in chat with “Ask about this lesson”.
- Ask the tutor: Send a question in chat; responses stream via SSE and cite retrieved sources.
- Practice: Generate a short quiz for a topic; submit answers and receive rubric‑based feedback.
- Build knowledge base: Upload textbooks/notes (PDF/MD). The system chunks, embeds, and indexes them for retrieval.
- Admin insights: Check simple analytics, trigger corpus reindexing, and manage content.

Getting Started

Option A — Docker Compose (recommended)
1) Prereqs: Docker Desktop (or Docker + Compose V2)
2) Copy env: `cp .env.example .env` and edit as needed (optional for dev)
3) Start stack: `make up`
   - Backend: http://localhost:8000 (health: `/healthz`)
   - Frontend: http://localhost:5173
- Postgres: `ankane/pgvector:pg16` with `vector` extension preinstalled
 - Postgres: `pgvector/pgvector:pg16` with `vector` extension preinstalled
4) Seed sample courses: `python llm-tutor/scripts/seed.py` (in a venv with backend deps) or add via DB.
5) Stop stack: `make down`

Option B — Local Dev (without Docker)
- Prereqs: Python 3.11, Node 20, Postgres 16 with `pgvector` extension, Redis 7
- Backend
  - Create venv; install deps: `pip install -U pip && pip install -e llm-tutor/backend[dev]`
  - Env vars (examples below). Then run: `bash llm-tutor/scripts/dev.sh`
  - On first run, the app ensures the `vector` extension, creates tables, and adds an HNSW index on `doc_chunks.embedding`.
- Frontend
  - `cd llm-tutor/frontend && npm install && npm run dev`
- Workers
  - `cd llm-tutor/backend && celery -A app.workers.celery_app.celery_app worker --loglevel=INFO`

Environment Variables (excerpt)
- `SECRET_KEY` (required): JWT signing key
- `DATABASE_URL`: e.g. `postgresql+psycopg://postgres:postgres@localhost:5432/llm_tutor`
- `REDIS_URL`: e.g. `redis://localhost:6379/0`
- `EMBEDDINGS_PROVIDER`: `fake` (default) or `openai`
- `OPENAI_API_KEY`: if using `openai` provider
- `OPENAI_BASE_URL`: optional OpenAI‑compatible endpoint
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default 15), `REFRESH_TOKEN_EXPIRE_DAYS` (default 7)
- `OTEL_EXPORTER_OTLP_ENDPOINT`, `SENTRY_DSN`: optional observability

Core Flows

Auth (email/password)
- Register: `POST /api/auth/register { email, password }`
- Login: `POST /api/auth/login { email, password }`
- Logout: `POST /api/auth/logout` (clears httpOnly refresh cookie)
Notes: Access token is returned in JSON; store it in memory (frontend does). The refresh token is set as an httpOnly cookie.

Documents & RAG
- Upload: `POST /api/documents/upload` (multipart) → fields: `file` (pdf|md), `course_id?`, `async_index` (default true)
- Reindex: `POST /api/rag/reindex` (admin) → schedules indexing jobs for all docs
- Search: `POST /api/rag/search { query, k }` → returns top‑k chunks with document titles
Pipeline: PDF/MD → extract text (pypdf for PDFs) → clean & chunk (~1200 chars, 200 overlap) → embeddings (pluggable) → pgvector store → HNSW index (cosine) → similarity search.

Chat (SSE)
- Create chat: `POST /api/chats` → `{ chat_id }`
- Send message: `POST /api/chats/{chat_id}/message { content, tools_allowed[] }`
- Stream response: `GET /api/chats/{chat_id}/stream` (SSE)
MVP streams simulated tokens; orchestration is wired to support retrieval and tool use.

Practice & Progress
- Generate quiz: `POST /api/tools/quiz/generate { topic|lesson_id, count, difficulty }`
- Grade quiz: `POST /api/tools/quiz/grade { answers }`
- My progress: `GET /api/progress/me`
- Complete a lesson: `POST /api/progress/lesson/{id}/complete`

Frontend
- Pages: `/login`, `/register`, `/courses`, `/lessons/:id`, `/chat/:chatId`, `/practice`, `/admin`
- Admin: FileDrop uploader for PDF/MD, reindex button, basic analytics placeholder
- Chat: Three‑pane layout (history, conversation, sources). Sources panel triggers RAG search and shows citation cards.

Running Tests & Formatting
- Backend tests: `cd llm-tutor/backend && pytest -q`
- Lint/format (backend): `ruff check . && ruff format .`
- Frontend build: `cd llm-tutor/frontend && npm run build`

Security & Compliance
- Passwords hashed with bcrypt; JWT with short‑lived access + httpOnly refresh cookie
- File uploads limited to PDF/MD; PDFs parsed as text only (no code execution)
- Simple rate limiting middleware enabled by default
- Code runner tool is disabled in MVP to avoid RCE; enable with a secure sandbox only
- See `llm-tutor/docs/SECURITY.md`

Performance & Observability
- SSE streaming for chat; optimistic UI on frontend
- pgvector HNSW index for similarity search
- Optional Sentry + OpenTelemetry tracing; see env vars

CI
- GitHub Actions: backend lint/test; frontend lint/build (`.github/workflows/ci.yml`)

Roadmap
- Real tutor orchestration with retrieval, planning, tool calls, and citations
- Code runner sandbox and result presentation in UI
- Quiz generation and rubric‑based grading powered by LLMs
- Admin CRUD for courses/modules/lessons; analytics dashboards
- Role‑based authorization; rate limit backed by Redis
- Alembic migrations for schema and vector indexes

Troubleshooting
- Port conflicts: change ports in `vite.config.ts` and compose
- pgvector errors locally: ensure `CREATE EXTENSION vector;` on your DB; compose uses `ankane/pgvector:pg16`
- Upload blocked: ensure you’re logged in so `Authorization` and cookies are present
- Worker not indexing: check Redis connectivity and Celery logs
