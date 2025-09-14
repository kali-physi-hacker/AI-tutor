from __future__ import annotations

import datetime as dt
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ..session import Base


class RoleEnum:
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(16), default=RoleEnum.student, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=dt.datetime.utcnow)

    @staticmethod
    async def get_by_id(session, user_id: int):
        from sqlalchemy import select

        res = await session.execute(select(User).where(User.id == user_id))
        return res.scalar_one_or_none()

    @staticmethod
    async def get_by_email(session, email: str):
        from sqlalchemy import select

        res = await session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()
