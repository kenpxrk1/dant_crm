import datetime
from uuid import UUID
from .repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db_manager
from sqlalchemy.orm import aliased
from sqlalchemy import ScalarResult, desc, func, insert, select, update, delete, join
from api.models.user import UserModel
from api.models.client import ClientModel
from api.models.appointments import AppointmentModel
from api.models.doctor import DoctorModel
from api.utils.hasher import HashingMixin
from sqlalchemy.exc import IntegrityError


class UserRepository(SQLAlchemyRepository):

    model = UserModel

    async def create_super_user(self, user_data: dict) -> None:
        async with db_manager.async_session() as session:
            try:
                super_user_query = select(self.model).where(user_data["login"] == self.model.login)
                user = await session.execute(super_user_query)
                if user.scalar_one_or_none() == None:
                    super_user_insert = insert(self.model).values(**user_data)
                    await session.execute(super_user_insert)
                    await session.commit()
            except IntegrityError:
                pass


    async def authenticate(self, username, password, session: AsyncSession) -> ScalarResult | None:
        stmt = select(self.model).where(username == self.model.login)
        user = await session.execute(stmt)
        user = user.scalars().first()

        if not user:
            return None
        if HashingMixin.verify(hashed_password=user.password, plain_password=password):
            return user
        else: 
            return None
        

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
        
        c = aliased(ClientModel)
        d = aliased(DoctorModel)
        a = aliased(AppointmentModel)
        select_query = (
            select(
                c.fullname.label("client_name"),
                c.date_of_birth.label("client_birthday"),
                c.phone_number.label("client_phone"),
                d.fullname.label("doctor_name"),
                d.phone_number.label("doctor_phone"),
                a.appointment_date,
                a.appointment_time,
            )
            .select_from(c)
            .join(a, a.client_id == c.id)
            .join(d, a.doctor_id == d.id)
        )
        res = await session.execute(select_query)
        return res.all()
    

    async def get_appointments_stats_for_doctors_by_occupation(self, period_from: datetime.date | None, period_to: datetime.date, session: AsyncSession):   
             

        """ Выборка количества записей для каждого врача 
        в период с datetime.date по datetime.date """

        a = aliased(AppointmentModel)
        d = aliased(DoctorModel)
        select_query = (
            select(                      
                d.occupation.label("occupation"),        
                func.count(a.id).label("appointments_counter")  
            )
            .select_from(d) 
            .join(a, d.id == a.doctor_id, isouter=True)
            .where(a.appointment_date.between(period_to, period_from))
            .group_by(d.occupation) 
            .order_by(desc(func.count(a.id)))
        )
        res = await session.execute(select_query)
        return res.all()

