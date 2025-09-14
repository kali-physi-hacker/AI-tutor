from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.deps import get_db
from ...db.models import Course, Module, Lesson

router = APIRouter()


@router.get("/courses")
async def list_courses(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course))
    items = res.scalars().all()
    return items


@router.get("/courses/{course_id}")
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.id == course_id))
    return res.scalar_one_or_none()


@router.get("/courses/{course_id}/modules")
async def list_modules(course_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Module).where(Module.course_id == course_id))
    return res.scalars().all()


@router.get("/modules/{module_id}/lessons")
async def list_lessons(module_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Lesson).where(Lesson.module_id == module_id))
    return res.scalars().all()


@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    return res.scalar_one_or_none()

