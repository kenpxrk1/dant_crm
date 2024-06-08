import datetime
import pandas as pd
from uuid import UUID
from fastapi import HTTPException, status
from pydantic import EmailStr
from api.repositories.appointments import AppointmentsRepository
from api.repositories.user import UserRepository
from api.schemas.user import UserReadDTO
from api.utils.hasher import HashingMixin
from api.config import super_user
from api.schemas.appointments import (
    AppointmentCreateDTO,
    AppointmentReadDTO,
    AppointmentsByConditionInput,
    AppointmentsByOccupation,
    JoinedAppointmentsDTO,
)
from api.utils.pdf_report import appointments_pdf
from api.tasks.tasks import send_appointments_report


class AppointmentsService:
    def __init__(self, repo: AppointmentsRepository) -> None:
        self.repo = repo

    async def create_appointment(
        self, appointment_data: AppointmentCreateDTO, session
    ) -> AppointmentReadDTO:
        
        appointment_data = appointment_data.model_dump()
        doctor_id = appointment_data['doctor_id']
        appointment_date = appointment_data['appointment_date']
        appointment_time = appointment_data['appointment_time']

        is_time_locked = await self.repo.can_schedule_appointment(doctor_id, appointment_date, appointment_time, session)

        if not is_time_locked:
                                                 
            raise HTTPException(
                status_code=400,
                detail="Время для записи занято"
            )
        
        if not await self.repo.is_doctor_workay(doctor_id, appointment_date, session):
            raise HTTPException(
                status_code=400,
                detail="Врач не работает в указанный день"
            )
        
        new_appmnt = await self.repo.create_appointment(appointment_data, session)
        return AppointmentReadDTO.model_validate(new_appmnt, from_attributes=True)

    async def get_appointments(self, session) -> list[JoinedAppointmentsDTO]:
        appointments = await self.repo.get_appointments(session)
        return [
            JoinedAppointmentsDTO.model_validate(appointment, from_attributes=True)
            for appointment in appointments
        ]

    async def get_appointments_stats_for_doctors_by_occupation(
        self, request: AppointmentsByConditionInput, session
    ) -> AppointmentsByOccupation:
        date_to, date_from = request.period_to, request.period_from
        appointments = await self.repo.get_appointments_stats_for_doctors_by_occupation(
            date_to, date_from, session
        )
        return [
            AppointmentsByOccupation.model_validate(appointment, from_attributes=True)
            for appointment in appointments
        ]

    async def appointments_to_pdf(self, email: EmailStr, session) -> None:
        appointments_tuple = await self.repo.get_appointments(session)
        appointments_df = pd.DataFrame(appointments_tuple)
        file_path = appointments_pdf.generate_path()
        pdf_data = appointments_pdf.create_report(file_path, appointments_df)
        send_appointments_report.delay(
            email=email,
            title="Отчет по записям в нашей клинике",
            pdf_buffer=pdf_data["buffer"],
            pdf_filename=pdf_data["file_name"],
        )
    

    async def delete_appointment(self, id: int, session):
        await self.repo.delete_appointment(id, session)

