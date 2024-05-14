import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from api.models.doctor import DoctorModel
from .repository import SQLAlchemyRepository
from api.models.days_off import DayOffModel
from api.schemas.days_off import ReadDaysOffDTO


class DoctorRepository(SQLAlchemyRepository):
    
    model = DoctorModel

    async def create_days_off(self, days_off_data: dict, id: int | UUID, session: AsyncSession) -> list[datetime.date]:
        new_days_off = []
        for day in days_off_data["days_off_date"]:
            new_day_off = DayOffModel(
                doctor_id = id,
                days_off_date = day
            )
            session.add(new_day_off)
            await session.flush()
            await session.commit()
            new_days_off.append(new_day_off.days_off_date)
        return new_days_off


    


        