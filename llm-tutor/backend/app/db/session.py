from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..core.config import settings


class Base(DeclarativeBase):
    pass


# Convert sync psycopg URL to async if needed
db_url = settings.database_url
if db_url.startswith("postgresql+") and "asyncpg" not in db_url:
    db_url = db_url.replace("psycopg", "asyncpg")

engine = create_async_engine(db_url, echo=False, pool_pre_ping=True)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)

