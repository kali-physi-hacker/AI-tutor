from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from sqlalchemy import text
from .db.session import engine, Base
from .db import models as _models  # noqa: F401
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .utils.rate_limit import SimpleRateLimitMiddleware

from .core.config import settings
from .utils.observability import setup_observability
from .api.router import api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting LLM Tutor Backend")
    setup_observability()
    # Ensure DB schema and vector extension exist (dev convenience)
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS idx_doc_chunks_embedding "
                    "ON doc_chunks USING hnsw (embedding vector_cosine_ops)"
                )
            )
    except Exception as e:
        logger.warning("DB init failed: %s", e)
    yield
    logger.info("Shutting down LLM Tutor Backend")


app = FastAPI(
    title="LLM Tutor API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(o) for o in settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.add_middleware(SimpleRateLimitMiddleware, limit=240, window_seconds=60)

app.include_router(api_router, prefix="/api")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}
