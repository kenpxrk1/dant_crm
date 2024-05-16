from fastapi import HTTPException
from sqlalchemy import Integer, ScalarResult, func, insert, select
from api.models.client import ClientModel
from api.repositories.repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.appointments import AppointmentModel
from sqlalchemy.exc import IntegrityError


class ClientRepository(SQLAlchemyRepository):
    
    model = ClientModel
    

    async def create_appointment(self, appointment_data: dict, session: AsyncSession) -> ScalarResult:
        try:
            appmnt_insert_query = insert(AppointmentModel).values(**appointment_data).returning(AppointmentModel)
            new_appmnt = await session.execute(appmnt_insert_query)
            await session.commit()
            new_appmnt = new_appmnt.scalar_one()
            return new_appmnt
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Invalid client or doctor id"
            )

    