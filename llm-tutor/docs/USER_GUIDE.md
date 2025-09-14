LLM Tutor — User Guide

Audience: learners (students) and operators (admins) using the LLM Tutor web app.

Overview
- Learn from structured courses and lessons.
- Ask the AI tutor questions with streaming, step‑by‑step answers and cited sources.
- Practice with auto‑generated quizzes and submit answers for feedback.
- Track lesson completion and revisit your chats.

Sign In & Accounts
- Create an account: open /register, enter email and password.
- Sign in: open /login, enter credentials. The app keeps you signed in with a secure refresh cookie.
- Sign out: use your browser to clear site data or add a sign‑out link if your deployment includes one.

Navigation
- Home: overview and quick links.
- Courses: list of available courses. Open a course to see its modules and lessons.
- Lesson: read Markdown content, code blocks, callouts, and math (where present).
- Chat: converse with the tutor, see live streaming replies, and browse sources.
- Practice: generate simple quizzes and prepare for assessments (MVP stub).
- Admin: upload documents (PDF/Markdown) to ground answers via retrieval; trigger reindex (admin only).

Courses & Lessons
- Browse courses at /courses.
- Click a course to view its modules and lessons.
- Open a lesson to read content and mark progress. When done, click “Complete” actions where available (or the UI will auto‑record completion in future iterations).

Chat with the Tutor
- Start a chat: navigate to /chat/:chatId (or via a UI link if present). New chat creation is handled by the backend endpoint and can be integrated into the UI.
- Ask a question: type your question and Send. The tutor streams a response token‑by‑token.
- Sources panel: use the search box to retrieve context chunks from the indexed documents; results list shows document titles and snippets you can skim while reading the answer.
- Tips for great results:
  - Ask focused questions tied to a lesson topic.
  - Upload your notes (PDF/MD) so the tutor can cite them later.
  - If unsure about context, run a quick search in the Sources panel first.

Practice (Quizzes)
- Navigate to /practice.
- Use the generator to produce practice questions (MVP displays placeholders). In future iterations, questions will be tailored by topic, difficulty, and lesson.
- Submit answers to receive feedback and a rubric (grading is currently stubbed for MVP).

Documents & Sources (RAG)
- Uploads: open /admin → “Upload Documents” and drop a PDF or Markdown file (UTF‑8).
  - Choose a Course ID (optional) to tag the document.
  - “Async index” schedules background indexing via the worker; disable to index inline.
- Reindex: on /admin, click “Reindex Corpus” to rebuild embeddings for all documents (admin‑gated in the API).
- Search: in the Chat Sources panel, enter a query to retrieve the top‑k similar chunks.
- Notes:
  - PDFs are parsed as text only; scanned documents without OCR will return little/no text.
  - Large files are chunked (~1200 chars with 200 overlap) and embedded into pgvector for fast similarity search.

Progress Tracking
- The system records lesson progress and quiz history (MVP stores completion events via the progress endpoints; UI indicators will evolve).
- Revisit lessons or chats anytime to reinforce concepts.

Accessibility & Performance
- High‑contrast color tokens and clear focus rings.
- Streamed responses (SSE) for fast feedback.
- Light animations mindful of motion sensitivity.

Troubleshooting
- Can’t sign in/register: ensure the backend is running and reachable; check that cookies are allowed for localhost.
- “Sources” are empty: upload course materials under /admin and wait for indexing (or disable async indexing), then try search again.
- Upload fails: confirm the file is PDF or Markdown and under your deployment’s size limits; ensure you are logged in.
- Streaming stops or disconnects: check network stability and reverse proxy/WebSocket/SSE configuration; the dev setup uses SSE over HTTP.
- Frontend shows 404: verify the route exists (e.g., /courses/:id) and that the backend endpoints return data.

Privacy
- The app stores minimal PII: email, password hash, and your learning artifacts (messages, progress). Keep your account private and avoid sharing sensitive data in uploads or chats.

What’s Next
- Deeper tutor orchestration with step planning, real tool calls, and inline citations.
- Richer quizzes with hints, solutions, and detailed grading.
- Admin dashboards, content authoring, and role‑based permissions.

