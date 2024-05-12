from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ScalarResult, insert, select, update, delete
from api.models.user import UserModel


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        """ Creates new row in database """
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        """ Returns all rows from database or None if its no one row in db """
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        """ Returns one row from database or error if query object doesnt exist"""
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        """ 
        Updated one row from database and returns new object or error 
        if query object doesnt exist 
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        """ Deletes one row from database and returns 200 status or error if query object doesnt exist """
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    model = None
    
    async def add_one(self, request_data: dict, session: AsyncSession) -> ScalarResult:
        insert_query = insert(self.model).values(**request_data).returning(self.model)
        result = await session.execute(insert_query)
        await session.commit()
        return result.scalar_one()

    async def find_all(self, session: AsyncSession) -> ScalarResult | None:
        select_query = select(self.model)
        result = await session.execute(select_query)
        result = result.scalars().all()
        if result == None:
            return None
        return result

    async def find_one(self, id: UUID, session: AsyncSession) -> ScalarResult | None:
        select_query = select(self.model).where(self.model.id == id)
        result = await session.execute(select_query)
        return result.scalar_one_or_none()

    async def update_one(self, request_data: dict, id: UUID, session: AsyncSession) -> ScalarResult | None:
        update_query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**request_data)
            .returning(self.model)
        )
        result = await session.execute(update_query)
        await session.commit()
        return result.scalar_one_or_none()

    async def delete_one(self, id: UUID, session: AsyncSession) -> None:
        delete_query = delete(self.model).where(self.model.id == id)
        await session.execute(delete_query)
        await session.commit()