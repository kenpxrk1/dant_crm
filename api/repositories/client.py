from sqlalchemy import Integer, ScalarResult, func, insert, select
from api.models.client import ClientModel
from api.repositories.repository import SQLAlchemyRepository
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


    async def get_appointments(self, session: AsyncSession) -> ScalarResult:
        """ SELECT 
	clients.fullname AS "client", 
	clients.date_of_birth,
	email, 
	clients.phone_number, 
	doctors.fullname AS "doctor",
	doctors.phone_number AS "doctors phone", 
	appointment_date, 
	appointment_time
    FROM 
    clients 
    INNER JOIN appointments ON clients.id = appointments.client_id
    INNER JOIN doctors ON appointments.doctor_id = doctors.id """