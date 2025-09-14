from __future__ import annotations

import io
import uuid
from typing import Literal

from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Document, DocChunk
from .chunking import chunk_text, simple_markdown_to_text, count_tokens_approx
from .embeddings import get_embeddings_client
from ..utils.paths import storage_dir


SourceType = Literal["pdf", "md", "url"]


async def save_document_record(db: AsyncSession, course_id: int | None, title: str, source_type: SourceType, path: str) -> Document:
    doc = Document(course_id=course_id, title=title, source_type=source_type, path=path)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def ingest_markdown(db: AsyncSession, title: str, md_bytes: bytes, course_id: int | None = None) -> dict:
    text = md_bytes.decode("utf-8", errors="ignore")
    clean = simple_markdown_to_text(text)
    filename = f"{uuid.uuid4().hex}.md"
    file_path = storage_dir() / filename
    file_path.write_bytes(md_bytes)
    doc = await save_document_record(db, course_id, title, "md", str(file_path))
    return await _index_text(db, doc, clean)


async def ingest_pdf(db: AsyncSession, title: str, pdf_bytes: bytes, course_id: int | None = None) -> dict:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text_parts: list[str] = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            pass
    text = "\n".join(text_parts)
    filename = f"{uuid.uuid4().hex}.pdf"
    file_path = storage_dir() / filename
    file_path.write_bytes(pdf_bytes)
    doc = await save_document_record(db, course_id, title, "pdf", str(file_path))
    return await _index_text(db, doc, text)


async def _index_text(db: AsyncSession, doc: Document, text: str) -> dict:
    chunks = chunk_text(text)
    if not chunks:
        return {"document_id": doc.id, "chunks": 0}
    embedder = get_embeddings_client()
    vectors = await embedder.embed(chunks)
    items: list[DocChunk] = []
    for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
        items.append(
            DocChunk(
                document_id=doc.id,
                chunk_index=i,
                text=chunk,
                embedding=vec,
                token_count=count_tokens_approx(chunk),
            )
        )
    db.add_all(items)
    await db.commit()

    return {"document_id": doc.id, "chunks": len(items)}

