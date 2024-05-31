import datetime
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from api.schemas.appointments import (
    AppointmentCreateDTO,
    AppointmentReadDTO,
    JoinedAppointmentsDTO,
    AppointmentsByOccupation,
    AppointmentsByConditionInput,
)
from api.dependencies import auth_service, get_appointments_service, doctor_service
from api.services.appointments import AppointmentsService
from api.schemas.user import UserReadDTO
from api.services.user import UserService
from api.db import db_manager
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.role_checker import RoleChecker

router = APIRouter(prefix="/appointments", tags=["AppointmentsData"])


@router.get("/report/pdf")
async def create_appointments_report(
    email: EmailStr,
    service: AppointmentsService = Depends(get_appointments_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    await service.appointments_to_pdf(email, session)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AppointmentReadDTO)
async def create_appointment(
    appointment_data: AppointmentCreateDTO,
    service: AppointmentsService = Depends(get_appointments_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    if await doctor_service.is_day_off(
        appointment_data.appointment_date, appointment_data.doctor_id, session
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The doctor is going to rest that day",
        )
    new_appointment = await service.create_appointment(appointment_data, session)
    return new_appointment


@router.get(
    "", status_code=status.HTTP_201_CREATED, response_model=list[JoinedAppointmentsDTO]
)
async def get_appointments(
    service: AppointmentsService = Depends(get_appointments_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    appointments = await service.get_appointments(session)
    return appointments


@router.get(
    "/report/occupation",
    status_code=status.HTTP_201_CREATED,
    response_model=list[AppointmentsByOccupation],
)
async def get_appointments_stats_for_doctors_by_occupation(
    date_from: datetime.date,
    date_to: datetime.date,
    service: AppointmentsService = Depends(get_appointments_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    request_data = AppointmentsByConditionInput(
        period_from=date_from, period_to=date_to
    )
    appointments = await service.get_appointments_stats_for_doctors_by_occupation(
        request_data, session
    )
    return appointments


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    id: int, 
    service: AppointmentsService = Depends(get_appointments_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),

):
    await service.delete_appointment(id, session)
