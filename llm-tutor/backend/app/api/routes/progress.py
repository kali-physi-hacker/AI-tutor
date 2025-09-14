from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.deps import get_db, get_current_user
from ...db.models import Progress, User

router = APIRouter()


@router.get("/me")
async def me(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    res = await db.execute(select(Progress).where(Progress.user_id == user.id))
    return res.scalars().all()


@router.post("/lesson/{lesson_id}/complete")
async def complete_lesson(lesson_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    prog = Progress(user_id=user.id, lesson_id=lesson_id, status="completed")
    db.add(prog)
    await db.commit()
    return {"ok": True}

