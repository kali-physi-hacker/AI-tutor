from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.deps import get_db, get_current_user
from ...services.rag import rag_search
from ...db.models import Document, User
from ...workers.tasks import index_document
from sqlalchemy import select

router = APIRouter()


class RAGSearchRequest(BaseModel):
    query: str
    k: int = 6


@router.post("/search")
async def search(req: RAGSearchRequest, db: AsyncSession = Depends(get_db)):
    return await rag_search(db, req.query, req.k)


@router.post("/reindex")
async def reindex(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    # naive admin check
    if getattr(user, "role", "student") != "admin":
        return {"status": "forbidden"}
    res = await db.execute(select(Document.id))
    ids = [row[0] for row in res.all()]
    for did in ids:
        index_document.delay(did)
    return {"status": "scheduled", "count": len(ids)}
