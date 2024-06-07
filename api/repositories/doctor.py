import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ScalarResult, insert, select
from api.models.doctor import DoctorModel
from .repository import SQLAlchemyRepository
from sqlalchemy.exc import IntegrityError


class DoctorRepository(SQLAlchemyRepository):

    model = DoctorModel
    
    async def search_by_fio(
            self,
            fullname: str, 
            session: AsyncSession,
    ) -> tuple:
        search_query = (
            select(self.model).where(self.model.fullname.ilike(f"%{fullname}%"))
        )
        search_query = await session.execute(search_query)
        search_result = search_query.scalars().all()
        return search_result
