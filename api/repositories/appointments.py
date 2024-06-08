import datetime
from uuid import UUID

from fastapi import HTTPException
from .repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db_manager
from sqlalchemy.orm import aliased
from sqlalchemy import ScalarResult, desc, func, insert, select, update, delete, join
from api.models.user import UserModel
from api.models.client import ClientModel
from api.models.appointments import AppointmentModel
from api.models.doctor import DoctorModel
from sqlalchemy.exc import IntegrityError
from api.models.working_hours import WorkingHoursModel, WeekDay


class AppointmentsRepository:

    async def get_appointments(self, session: AsyncSession) -> ScalarResult:
        """SELECT
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
        INNER JOIN doctors ON appointments.doctor_id = doctors.id"""

        c = aliased(ClientModel)
        d = aliased(DoctorModel)
        a = aliased(AppointmentModel)
        select_query = (
            select(
                a.id,
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

    async def get_appointments_stats_for_doctors_by_occupation(
        self,
        period_from: datetime.date | None,
        period_to: datetime.date,
        session: AsyncSession,
    ):
        """Выборка количества записей для каждого врача
        в период с datetime.date по datetime.date"""

        a = aliased(AppointmentModel)
        d = aliased(DoctorModel)
        select_query = (
            select(
                d.occupation.label("occupation"),
                func.count(a.id).label("appointments_counter"),
            )
            .select_from(d)
            .join(a, d.id == a.doctor_id, isouter=True)
            .where(a.appointment_date.between(period_to, period_from))
            .group_by(d.occupation)
            .order_by(desc(func.count(a.id)))
        )
        res = await session.execute(select_query)
        return res.all()
    
    async def create_appointment(
        self, appointment_data: dict, session: AsyncSession
    ) -> ScalarResult:
        try:
            appmnt_insert_query = (
                insert(AppointmentModel)
                .values(**appointment_data)
                .returning(AppointmentModel)
            )
            new_appmnt = await session.execute(appmnt_insert_query)
            await session.commit()
            new_appmnt = new_appmnt.scalar_one()
            return new_appmnt
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid client or doctor id")

    async def delete_appointment(
            self,
            id: int,
            session: AsyncSession
    ) -> None:
        delete_stmt = (
            delete(AppointmentModel).where(AppointmentModel.id == id)
        )
        await session.execute(delete_stmt)
        await session.commit()

    async def can_schedule_appointment(self, doctor_id: UUID, appointment_date: datetime.date,
                                       appointment_time: datetime.time, session: AsyncSession) -> bool:
        one_hour = datetime.timedelta(hours=1)
        start_time = datetime.datetime.combine(appointment_date, appointment_time)
        end_time = start_time + one_hour

        select_overlapping_appointments = (
            select(AppointmentModel)
            .where(
                AppointmentModel.doctor_id == doctor_id,
                AppointmentModel.appointment_date == appointment_date,
                AppointmentModel.appointment_time >= (start_time - one_hour).time(),
                AppointmentModel.appointment_time < end_time.time()
                )
        )
        overlapping_appointments = await session.execute(select_overlapping_appointments)
        overlapping_appointments = overlapping_appointments.all()
        return len(overlapping_appointments) == 0
    
    async def is_doctor_workay(self, doctor_id: UUID, appointment_date: datetime.date, session: AsyncSession):

        """ Если рабочий день возвращает True, 
         в противном случае - False """

        week_day_number = appointment_date.isoweekday()
        week_day = WeekDay.get_weekday_by_number(week_day_number)
        select_query = (
            select(WorkingHoursModel)
            .where(
                WorkingHoursModel.doctor_id == doctor_id, 
                WorkingHoursModel.day_of_week == week_day
                )
        )
        result = await session.execute(select_query)
        result = result.all()
        return len(result) != 0
