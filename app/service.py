from typing import Optional

from sqlalchemy import select, insert, delete
from app.database import async_session
from app.models import Task

class TaskService:
    model = Task
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = (
                select(cls.model).filter_by(**filter_by)
            )
            result = await session.execute(query)
            return result.scalars().all()
    @classmethod
    async def get_by_number(cls, number: int) -> Optional[Task]:
        async with async_session() as session:
            query = select(cls.model).filter_by(number=number)
            result = await session.execute(query)
            return result.scalars().first()
    @classmethod
    async def add(cls, number: int, title: str, description: str):
        async with async_session() as session:
            query = (
                insert(cls.model).values(number=number, title=title, description=description)
            )
            await session.execute(query)
            await session.commit()

            return await cls.get_by_number(number=number)

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session() as session:
            query = (
                delete(cls.model).filter_by(**filter_by)
            )
            await session.execute(query)
            await session.commit()