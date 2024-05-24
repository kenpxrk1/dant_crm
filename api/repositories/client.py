from fastapi import HTTPException
from sqlalchemy import Integer, ScalarResult, func, insert, select
from api.models.client import ClientModel
from api.repositories.repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.appointments import AppointmentModel
from sqlalchemy.exc import IntegrityError


class ClientRepository(SQLAlchemyRepository):

    model = ClientModel

    async def search_by_fio(
        self,
        fullname: str,
        session: AsyncSession,
    ) -> ScalarResult:
        search_query = select(self.model).where(
            self.model.fullname.ilike(f"%{fullname}%")
        )
        search_query = await session.execute(search_query)
        search_result = search_query.scalars().all()
        return search_result
