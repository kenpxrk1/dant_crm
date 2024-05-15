from sqlalchemy import ScalarResult, insert
from api.models.client import ClientModel
from api.repositories.repository import SQLAlchemyRepository
from api.schemas.appointments import AppointmentReadDTO
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.appointments import AppointmentModel


class ClientRepository(SQLAlchemyRepository):
    
    model = ClientModel

    async def create_appointment(self, appointment_data: dict, session: AsyncSession) -> ScalarResult:
        appmnt_insert_query = insert(AppointmentModel).values(**appointment_data).returning(AppointmentModel)
        new_appmnt = await session.execute(appmnt_insert_query)
        await session.commit()
        new_appmnt = new_appmnt.scalar_one()
        return new_appmnt
