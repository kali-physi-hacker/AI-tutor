
You are a senior full-stack engineer AI coding agent. Build a production-ready LLM Tutor platform that helps learners study courses (STEM focus), chat with an AI tutor, get step-by-step explanations, generate practice questions, evaluate answers, and track progress. Optimize for reliability, testability, performance, and speed of iteration. Ship a working MVP with room to scale.

1) Core Requirements (MVP)
	•	Users & Auth: Email/password + Google OAuth. JWT access/refresh (httpOnly refresh cookie). Roles: student, admin.
	•	Content: Course → Module → Lesson hierarchy (markdown, code blocks, images). PDF/MD upload; automatic chunking + embeddings for retrieval.
	•	Tutor Chat: System/user/tool messages; tools: Retrieval (RAG), Code Runner (sandboxed), Web Math (symbolic/LaTeX), Quiz Generator, Grader. Tutor answers step-by-step with citations and inline math.
	•	Practice & Assessment: Auto-generated quizzes (MCQ/short/code), hints, solution keys. LLM-aided grading with rubric + score + feedback.
	•	Progress: Track lessons, quiz history, topic mastery, time-on-task.
	•	Admin: CRUD courses/modules/lessons, upload docs, view analytics, re-embed corpus.

Non-Functional: typed code, clean modular architecture, 80% unit coverage on core; streaming responses; basic metrics & error tracking; input validation; rate limits; secrets in env; minimal PII.

2) Tech Stack
	•	Backend: Python 3.11, FastAPI (async), PostgreSQL + pgvector, SQLAlchemy 2.x, Alembic.
	•	Embeddings & LLMs: Provider interface (OpenAI-compatible), embeddings stored in pgvector.
	•	Async/Jobs: Celery + Redis (embedding, grading, long-running tasks).
	•	Realtime: SSE for streaming chat.
	•	Frontend: React + TypeScript + Vite, TailwindCSS, shadcn/ui, Zustand, React Router, Framer Motion.
	•	Auth: JWT (httpOnly refresh cookie; access token in memory).
	•	Containers/CI: Docker (+ docker-compose dev), GitHub Actions (lint/type/test/build).
	•	Observability: OpenTelemetry hooks (basic), Sentry optional via env.
	•	Testing: Pytest; Vitest + Playwright (smoke).

3) Repository Layout

llm-tutor/
  backend/
    app/
      api/            # routers
      core/           # settings, deps, security
      db/             # models, schemas, migrations
      services/       # rag, tutor, quiz, grader, code_runner
      workers/        # celery tasks
      utils/
      main.py
    tests/
    alembic/
    pyproject.toml
  frontend/
    src/
      components/
      pages/
      hooks/
      store/
      lib/
      App.tsx
      main.tsx
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
    ARCHITECTURE.md
    API.md
    RAG.md
    SECURITY.md
  .github/workflows/ci.yml
  .env.example
  Makefile
  README.md

4) Data Model (Postgres)
	•	users(id, email UNIQUE, password_hash, role, created_at)
	•	courses(id, title, description, slug, created_at, updated_at)
	•	modules(id, course_id FK, title, index)
	•	lessons(id, module_id FK, title, slug, content_md, index)
	•	documents(id, course_id FK NULL, title, source_type[pdf|url|md], path/url)
	•	doc_chunks(id, document_id FK, chunk_index, text, embedding vector(1536), token_count)
	•	chats(id, user_id FK, course_id FK NULL, title, created_at)
	•	messages(id, chat_id FK, role[system|user|assistant|tool], content_json, created_at, token_usage_json)
	•	quizzes(id, user_id FK, course_id FK NULL, spec_json, created_at)
	•	quiz_items(id, quiz_id FK, type[mcq|short|code], question_md, options_json, correct_json)
	•	quiz_submissions(id, quiz_id FK, user_id FK, submitted_at, score, rubric_json, feedback_md)
	•	progress(id, user_id FK, lesson_id FK, status[started|completed], first_seen_at, completed_at)
	•	eval_runs(id, name, spec_json, metrics_json, created_at)

Indexes: users.email, doc_chunks.embedding (HNSW), messages.chat_id, progress.user_id+lesson_id.

5) API (FastAPI)

Auth:
POST /api/auth/register · POST /api/auth/login · POST /api/auth/refresh · POST /api/auth/logout

Catalog:
GET /api/courses · GET /api/courses/{id} · GET /api/courses/{id}/modules · GET /api/modules/{id}/lessons · GET /api/lessons/{id}

Documents & RAG:
POST /api/documents/upload (async index) · POST /api/rag/reindex (admin) · POST /api/rag/search {query,k} → chunks

Chat (SSE):
POST /api/chats → {chat_id} · GET /api/chats/{chat_id}/stream (SSE tokens) · POST /api/chats/{chat_id}/message {content,tools_allowed[]} → 202

Tools:
POST /api/tools/code-run {language, code, tests?} → {stdout, stderr, results}
POST /api/tools/quiz/generate {topic|lesson_id, count, difficulty} → quiz draft
POST /api/tools/quiz/grade {answers} → {score, rubric, feedback_md}
POST /api/tools/math/solve {latex|text} → {steps_md, result}

Progress & Analytics:
GET /api/progress/me · POST /api/progress/lesson/{id}/complete · GET /api/admin/analytics (admin)

Admin: CRUD endpoints for courses/modules/lessons (protected).
Provide OpenAPI docs + docs/API.md examples.

6) Tutor Orchestration
	•	System Prompt (store in services/tutor/prompts.py): expert STEM teacher; reason step-by-step; adapt level; never fabricate citations; ask clarifying Qs when unsure; concise hints; minimal LaTeX; use Tools interface.
	•	Tools: search_context(query,k=6), run_code(language,code), generate_quiz(topic,count,difficulty), grade_freeform(answer,rubric).
	•	Policy: For each query: retrieve context → plan → call tools → produce answer with citations (chunk→doc mapping). Stream; cache per-chat RAG hits.

7) Frontend (React) — Distinct UI/UX & Motion Integrated

Pages
	•	/login, /register
	•	/courses, /courses/:id, /lessons/:id
	•	/chat/:chatId (left rail history · content pane chat · right drawer Sources/Tools)
	•	/practice (quiz generate/submit)
	•	/admin (CRUD, reindex)

Components

ChatMessage, SSEStream, CitationsPanel, CodeRunner, QuizCard, ProgressRadar, LessonViewer (markdown+math), FileDrop, CommandPalette (⌘K), ConceptChip.

UI/UX & Motion Spec — Make It Distinct (non-generic)

Visual Identity
	•	Design keywords: calm, expert, scholastic, modern, trustworthy.
	•	Brand motif: subtle geometric “concept graph” dots/lines in headers & empty states (SVG @ 2–4% opacity).
	•	Type: Display --font-display (e.g., Satoshi/Outfit/Geist → fallback system-ui); Text --font-text (Inter/IBM Plex Sans). Tight headings; comfy body line-height.
	•	Colors (light/dark high-contrast):
	•	Light: bg:#FAFAFC, card:#FFFFFF, ink #12131A, primary #3A5BF5, accent #16A394, warning #D97706.
	•	Dark: bg:#0C0F14, card:#11151D, ink #E8EAF2, primary #6C89FF, accent #4CCFBF.
	•	Elevation: rounded-2xl, shadow-[0_8px_30px_rgba(0,0,0,0.06)].

Layout
	•	Grid: max-w 1200px center; 12-col / 24px gutters.
	•	Density: compact for chat/citations; spacious for lesson reading.
	•	Navigation: left rail (history), content (chat/lesson), right drawer (sources/tools). Collapsible for md; overlay drawers on mobile.

Motion (Framer Motion)
	•	Philosophy: invisible but felt. Micro-interactions 120–180ms; page transitions 220–280ms; spring {stiffness:300, damping:30}.
	•	Page transition: fade + 10px slide-up.
	•	Chat streaming: type-on reveal; caret blink 750ms; 50ms stagger per line.
	•	Buttons: active: scale 0.99; hover lifts shadow.
	•	Drawers: 24px slide + fade; backdrop blur.
	•	Quiz: correct → tiny confetti (800ms); incorrect → gentle shake (±4px, 120ms).
	•	Respect prefers-reduced-motion by auto-disabling nonessential animations.

Distinct Components
	•	ConceptChip: pill with progress dot (ring gradient primary→accent).
	•	CitationsPanel: masonry of sources with favicon, confidence bar, “jump to paragraph.”
	•	CodeRunner: split editor/output; sticky “Run tests”; auto-scroll to first failure.
	•	LessonViewer: MD+math with callouts (Tip/Warning/Definition); “Try in Chat” inline CTA to seed prompts.
	•	ProgressRadar: Recharts radar with subtle glow; hover shows rubric.
	•	Command Palette (⌘K): search courses, lessons, recent chats, commands (Generate quiz, Reindex, New chat).

Microcopy & Empty States
	•	Chat: “Ask about today’s lesson or drop a PDF—your tutor cites sources.”
	•	RAG: “No sources yet. Upload notes or open a lesson to ground answers.”
	•	Quiz: “Pick a topic & difficulty; I’ll craft 5 questions with hints.”

Responsiveness
	•	Breakpoints: sm 360, md 768, lg 1024, xl 1280.
	•	Mobile: bottom tab bar (Home, Learn, Chat, Practice); full-screen drawers for Sources/Tools; composer never covered by keyboard.
	•	Tablet: two-pane; sources as side drawer.
	•	Desktop: three-pane.

Accessibility (WCAG 2.1 AA)
	•	Contrast ≥ 4.5:1; visible focus rings outline-2 outline-offset-2 outline-primary.
	•	Full keyboard nav; skip links; roving tab index for lists.
	•	Streaming uses aria-live="polite"; pause/resume stream control.

Performance & Perceived Speed
	•	Skeletons everywhere; optimistic UI for sending messages.
	•	Route code-splitting; prefetch on hover.
	•	SVG motifs; lazy-load heavy images.

Tailwind Tokens (add to tailwind.config.js)

extend:{
  borderRadius:{ xl:'1rem', '2xl':'1.25rem' },
  boxShadow:{ card:'0 8px 30px rgba(0,0,0,0.06)', lift:'0 12px 40px rgba(0,0,0,0.10)' },
  colors:{
    ink:{ DEFAULT:'#12131A', soft:'#2A2C36', inverted:'#E8EAF2' },
    paper:{ DEFAULT:'#FAFAFC', raised:'#FFFFFF', sunken:'#F3F5F9' },
    primary:{ DEFAULT:'#3A5BF5', soft:'#6C89FF' },
    accent:{ DEFAULT:'#16A394', soft:'#4CCFBF' },
  }
}

Reusable Animation Helpers
	•	Page wrapper (fade/slide), list staggerChildren(50ms).
	•	Utilities: .pressable (active scale), .elevate (hover shadow), .smooth (duration-200).

Concrete Flows
	•	Chat composer: multiline + slash-commands (/sources on|off, /quiz 5 medium Calculus); toolbar: Cite toggle, Copy, Export MD, Regenerate, Explain code; token count + elapsed micro-stats.
	•	Lesson → Chat handoff: highlight → mini menu (Explain, Quiz me, Add to notes); seed chat with selection + lesson link; auto-attach citations.
	•	Quiz: topic + difficulty + type; start with progress ring & “focus mode”; results show score, rubric, links to lesson sections; “retry weak concepts.”

Theming Hooks
	•	CSS vars: --brand-hue, --brand-sat, --brand-primary, --brand-accent. Persist theme per user.

UI Definition of Done
	•	No layout jumps > 8px during stream; 60fps on modern laptop; heavy ops async.
	•	Keyboard-only path covers: login → lesson → chat → citations → quiz → submit.
	•	All interactives have focus styles + accessible names.
	•	Mobile drawers swipeable; composer always visible.

Telemetry
	•	Events: chat_started, token_stream_complete, citation_opened, quiz_generated, quiz_submitted, lesson_to_chat_handoff.
	•	KPIs: time-to-first-token, citation open rate, quiz completion rate, % answers with citations, retry rate.

Anti-Goals
	•	No stock templates or over-animation; no blocking loaders; avoid modals for long content (use drawers/routes).

Example Stubs

// components/Page.tsx
import { motion } from "framer-motion";
export default function Page({ children }: { children: React.ReactNode }) {
  return (
    <motion.main initial={{opacity:0,y:10}} animate={{opacity:1,y:0}} transition={{duration:0.22}}
      className="mx-auto w-full max-w-[1200px] px-4 md:px-6">{children}</motion.main>
  );
}

// components/Stagger.tsx
import { motion } from "framer-motion";
export const Stagger = ({children}:{children:React.ReactNode}) => (
  <motion.div variants={{show:{transition:{staggerChildren:0.05}}}} initial="show">{children}</motion.div>
);
export const Item = ({children}:{children:React.ReactNode}) => (
  <motion.div variants={{hidden:{opacity:0,y:4},show:{opacity:1,y:0,transition:{duration:0.16}}}}>
    {children}
  </motion.div>
);

8) Security & Compliance

Validate inputs (Pydantic), sanitize markdown, escape math. Sandbox code exec (firejail/docker; cpu/mem/fs/net limits). Rate limits per IP/user on chat & tools. Data minimization; account deletion; export stub. Secrets via env only.

9) Observability

Structured JSON logs (request_id, user_id). Error tracking (Sentry via env). Metrics: latency/success, tokens used, RAG hit rate, quiz gen time.

10) CI/CD & Dev Ex

Makefile: make dev, make test, make lint, make up, make migrate, make seed.
GitHub Actions: ruff, mypy, pytest; eslint, tsc, vitest; build & push Docker images.
docker-compose (dev): postgres (pgvector), redis, backend, worker, frontend, optional reverse proxy.

11) Configuration (.env.example)

APP_ENV=dev
SECRET_KEY=change-me
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/tutor
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=
LLM_PROVIDER=openai
EMBED_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
SENTRY_DSN=
ALLOW_GOOGLE_OAUTH=true
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
VITE_API_BASE=http://localhost:8000

12) Testing Strategy

Backend: unit tests for RAG (chunk/index/search), tutor planner, tool adapters, grading rubric, auth; integration for chat flow and upload→embed→search.
Frontend: Vitest for UI logic; Playwright smoke (login, open course, chat, generate quiz, submit, view progress).
Eval Harness: eval_runs benchmark Q&A with expected key points; judge answer quality, citation presence, hallucination rate.

13) Deliverables
	•	One-command dev run via docker-compose up.
	•	Seed data: Course “Calculus I” (3 modules, 6 lessons), sample PDFs embedded & searchable, demo user student@example.com / password.
	•	Screens: course catalog, lesson view with “Ask Tutor,” chat with streaming + citations, quiz generate/submit + grading, admin upload & reindex.
	•	Docs: README.md (quickstart), ARCHITECTURE.md, API.md, RAG.md, SECURITY.md.

14) Definition of Done (MVP)
	•	User signs in, opens a lesson, asks a question, sees streamed tutor response with citations.
	•	User generates a quiz, answers, and receives graded feedback + score.
	•	Admin uploads a PDF and reindexes, and those chunks appear in RAG.
	•	80% coverage on services/rag, services/tutor, api/auth. CI green. No plaintext secrets committed.

15) Stretch (Time-Permitting)

Spaced repetition (SM-2), multi-provider LLM failover + cost tracking, finer-grained mastery graph.

Build Steps (for the Coding Agent)
	1.	Scaffold repo as above.
	2.	Implement DB models + Alembic migrations.
	3.	Implement Auth, Catalog, RAG (ingest→chunk→embed→store), Chat SSE with tool calling.
	4.	Build React UI per the Distinct UI/UX & Motion spec.
	5.	Add Celery workers for embeddings/grading.
	6.	Add tests & CI.
	7.	Provide seed data; ensure docker-compose up launches a working demo.

When ambiguities arise, choose sensible defaults and keep interfaces clean for iteration.