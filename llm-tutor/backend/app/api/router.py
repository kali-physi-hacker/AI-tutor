from __future__ import annotations

from fastapi import APIRouter

from .routes import auth, catalog, rag, chat, tools, progress, admin, documents

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(catalog.router, tags=["catalog"])
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
api_router.include_router(chat.router, prefix="/chats", tags=["chat"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
