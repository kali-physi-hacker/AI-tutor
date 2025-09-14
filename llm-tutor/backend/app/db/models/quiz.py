from __future__ import annotations

import datetime as dt
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..session import Base


class Quiz(Base):
    __tablename__ = "quizzes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    spec_json: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=dt.datetime.utcnow)
    items: Mapped[list[QuizItem]] = relationship("QuizItem", back_populates="quiz")


class QuizItem(Base):
    __tablename__ = "quiz_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(16))  # mcq|short|code
    question_md: Mapped[str] = mapped_column(Text)
    options_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    correct_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    quiz: Mapped[Quiz] = relationship("Quiz", back_populates="items")


class QuizSubmission(Base):
    __tablename__ = "quiz_submissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    submitted_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=dt.datetime.utcnow)
    score: Mapped[float | None] = mapped_column()
    rubric_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    feedback_md: Mapped[str | None] = mapped_column(Text, nullable=True)

