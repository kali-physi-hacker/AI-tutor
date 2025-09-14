import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import async_session
from app.db.models import Course


async def main():
    async with async_session() as session:  # type: AsyncSession
        res = await session.execute(select(Course))
        if not res.scalars().first():
            session.add(Course(title="Calculus I", description="Limits and derivatives", slug="calculus-i"))
            session.add(Course(title="Linear Algebra", description="Vectors and matrices", slug="linear-algebra"))
            await session.commit()
            print("Seeded courses")
        else:
            print("Courses already present")


if __name__ == "__main__":
    asyncio.run(main())

