import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ScalarResult, insert, select
from api.models.doctor import DoctorModel
from .repository import SQLAlchemyRepository
from sqlalchemy.exc import IntegrityError
from api.models.working_hours import WorkingHoursModel

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


    async def create_working_hours(self, data: dict, session: AsyncSession):
        try:
            insert_query = (
                insert(WorkingHoursModel)
                .values(**data)
                .returning(WorkingHoursModel)
                )
            new_wh = await session.execute(insert_query)
            await session.commit()
            new_wh = new_wh.scalar_one()
            return new_wh
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid doctor id")