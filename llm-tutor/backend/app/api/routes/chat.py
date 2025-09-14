from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.deps import get_db, get_current_user
from ...db.models import Chat, Message, User
from ...services.tutor.orchestrator import stream_tutor_response

router = APIRouter()


class CreateChatRequest(BaseModel):
    title: str | None = None
    course_id: int | None = None


@router.post("")
async def create_chat(
    body: CreateChatRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    chat = Chat(user_id=user.id, title=body.title or "New chat", course_id=body.course_id)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return {"chat_id": chat.id}


class MessageRequest(BaseModel):
    content: str
    tools_allowed: list[str] | None = None


@router.post("/{chat_id}/message", status_code=202)
async def post_message(
    chat_id: int,
    body: MessageRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    chat = await db.get(Chat, chat_id)
    if not chat or chat.user_id != user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    msg = Message(chat_id=chat_id, role="user", content_json={"text": body.content})
    db.add(msg)
    await db.commit()
    return {"accepted": True}


@router.get("/{chat_id}/stream")
async def stream(chat_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    chat = await db.get(Chat, chat_id)
    if not chat or chat.user_id != user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    generator = stream_tutor_response(db, chat_id)
    return EventSourceResponse(generator, media_type="text/event-stream")

