from __future__ import annotations

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..session import Base
from pgvector.sqlalchemy import Vector


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(16))
    path: Mapped[str] = mapped_column(Text)  # path or URL

    chunks: Mapped[list[DocChunk]] = relationship("DocChunk", back_populates="document")


class DocChunk(Base):
    __tablename__ = "doc_chunks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    document: Mapped[Document] = relationship("Document", back_populates="chunks")
