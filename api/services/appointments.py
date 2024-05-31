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

