from __future__ import annotations

from .celery_app import celery_app
from ..services.ingest import _index_text  # type: ignore
from ..db.session import async_session
from ..db.models import Document
from sqlalchemy import select


@celery_app.task(name="app.workers.tasks.embed_document")
def embed_document(document_id: int) -> dict[str, int]:
    # Placeholder: simulate embedding work
    return {"document_id": document_id}


@celery_app.task(name="app.workers.tasks.grade_quiz")
def grade_quiz(quiz_submission_id: int) -> dict[str, int]:
    return {"quiz_submission_id": quiz_submission_id}


@celery_app.task(name="app.workers.tasks.index_document")
def index_document(document_id: int) -> dict[str, int]:
    # Run indexing in a synchronous loop using async session
    import asyncio

    async def run():
        async with async_session() as session:
            res = await session.execute(select(Document).where(Document.id == document_id))
            doc = res.scalar_one()
            from ..services.ingest import _index_text as index_text
            from pypdf import PdfReader
            import io
            with open(doc.path, "rb") as f:
                data = f.read()
            if doc.source_type == "pdf":
                try:
                    reader = PdfReader(io.BytesIO(data))
                    text_parts = [(p.extract_text() or "") for p in reader.pages]
                    text = "\n".join(text_parts)
                except Exception:
                    text = ""
            else:
                text = data.decode("utf-8", errors="ignore")
            return await index_text(session, doc, text)

    result = asyncio.get_event_loop().run_until_complete(run())
    return {"document_id": document_id, **{k: v for k, v in result.items() if isinstance(v, int)}}
