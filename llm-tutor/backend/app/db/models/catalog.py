from __future__ import annotations

import datetime as dt
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..session import Base


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=dt.datetime.utcnow)

    modules: Mapped[list[Module]] = relationship("Module", back_populates="course")


class Module(Base):
    __tablename__ = "modules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    index: Mapped[int] = mapped_column(Integer, default=0)

    course: Mapped[Course] = relationship("Course", back_populates="modules")
    lessons: Mapped[list[Lesson]] = relationship("Lesson", back_populates="module")


class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255))
    content_md: Mapped[str] = mapped_column(Text)
    index: Mapped[int] = mapped_column(Integer, default=0)

    module: Mapped[Module] = relationship("Module", back_populates="lessons")

