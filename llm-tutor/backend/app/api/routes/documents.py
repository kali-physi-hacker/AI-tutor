from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.deps import get_db, get_current_user
from ...db.models import User
from ...services.ingest import ingest_markdown, ingest_pdf, save_document_record
from ...utils.paths import storage_dir
from ...workers.tasks import index_document
import uuid

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    course_id: int | None = Form(default=None),
    async_index: bool = Form(default=True),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Only students/admins with session can upload; basic guard present
    content = await file.read()
    ct = (file.content_type or "").lower()
    title = file.filename or "Untitled"
    try:
        is_pdf = ct.endswith("pdf") or ct == "application/pdf" or title.lower().endswith(".pdf")
        is_md = ("markdown" in ct) or title.lower().endswith(".md") or ct == "text/plain"
        if not (is_pdf or is_md):
            raise HTTPException(status_code=400, detail=f"Unsupported content type: {ct}")

        if async_index:
            # Save file to storage and create Document record, schedule indexing
            ext = ".pdf" if is_pdf else ".md"
            filename = f"{uuid.uuid4().hex}{ext}"
            path = storage_dir() / filename
            path.write_bytes(content)
            doc = await save_document_record(db, course_id, title, "pdf" if is_pdf else "md", str(path))
            index_document.delay(doc.id)
            return {"ok": True, "document_id": doc.id, "chunks": 0, "scheduled": True}
        else:
            if is_pdf:
                res = await ingest_pdf(db, title=title, pdf_bytes=content, course_id=course_id)
            else:
                res = await ingest_markdown(db, title=title, md_bytes=content, course_id=course_id)
            return {"ok": True, **res}
    finally:
        await file.close()
