from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db.models import DocChunk, Document
from .embeddings import get_embeddings_client


async def rag_search(db: AsyncSession, query: str, k: int = 6):
    embedder = get_embeddings_client()
    [qvec] = await embedder.embed([query])
    distance = DocChunk.embedding.cosine_distance(qvec)
    stmt = (
        select(DocChunk, Document)
        .join(Document, Document.id == DocChunk.document_id)
        .order_by(distance)
        .limit(k)
    )
    res = await db.execute(stmt)
    rows = res.all()
    chunks = [
        {
            "chunk_id": dc.id,
            "document_id": doc.id,
            "document_title": doc.title,
            "chunk_index": dc.chunk_index,
            "text": dc.text[:5000],
        }
        for (dc, doc) in rows
    ]
    return {"query": query, "k": k, "chunks": chunks}
