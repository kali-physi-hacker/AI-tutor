API Overview

Auth
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout

Catalog
- GET /api/courses
- GET /api/courses/{id}
- GET /api/courses/{id}/modules
- GET /api/modules/{id}/lessons
- GET /api/lessons/{id}

Documents
- POST /api/documents/upload (multipart): fields: file (pdf|md), course_id (optional), async_index (bool, default true)
- Response: { ok, document_id, chunks, scheduled? }

RAG
- POST /api/rag/search {query,k}
- POST /api/rag/reindex

Chat (SSE)
- POST /api/chats → {chat_id}
- POST /api/chats/{chat_id}/message
- GET /api/chats/{chat_id}/stream (SSE)

Tools
- POST /api/tools/code-run
- POST /api/tools/quiz/generate
- POST /api/tools/quiz/grade
- POST /api/tools/math/solve

Progress
- GET /api/progress/me
- POST /api/progress/lesson/{id}/complete

Admin
- GET /api/admin/analytics
