RAG Design

- Documents are uploaded (PDF/MD/URL) and chunked; chunks are embedded and stored.
- Search computes embedding for query and retrieves top-k similar chunks.
- Tutor orchestrator cites sources; maps chunks back to documents.

MVP Implementation

- Upload supports PDF/Markdown. Text is extracted then chunked (~1200 chars, 200 overlap).
- Embeddings provider is pluggable via `EMBEDDINGS_PROVIDER` (fake|openai). Fake provider is default for offline dev.
- Embeddings stored in pgvector column `doc_chunks.embedding (vector(1536))` with HNSW index for cosine similarity.
- Search computes embedding for the query and retrieves top-k chunks ordered by cosine distance.
