from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/analytics")
async def analytics():
    # Placeholder metrics
    return {"users": 0, "chats": 0, "messages": 0}

