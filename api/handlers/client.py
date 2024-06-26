from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies import (
    get_client_service,
    ClientService,
    auth_service,
    doctor_service,
)
from api.schemas.client import (
    ClientCreateDTO,
    ClientReadDTO,
    ClientUpdateDTO,
    CountClientDTO,
    SearchClientDTO
)
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db_manager
from api.schemas.user import UserReadDTO
from api.utils.role_checker import RoleChecker
from api.schemas.appointments import AppointmentCreateDTO, AppointmentReadDTO
from api.schemas.mail import CreateMail


router = APIRouter(prefix="/clients", tags=["Client"])


@router.post("", response_model=ClientReadDTO, status_code=status.HTTP_201_CREATED)
async def add_new_client(
    client_data: ClientCreateDTO,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    new_doctor = await service.add_client(client_data, session)
    return new_doctor


@router.get("", response_model=list[ClientReadDTO], status_code=status.HTTP_200_OK)
async def get_clients(
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    clients = await service.get_clients(session)
    return clients


@router.put("/{id}", response_model=ClientReadDTO, status_code=status.HTTP_201_CREATED)
async def update_clients(
    client_data: ClientUpdateDTO,
    id: UUID,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    update_client = await service.update_doctor(client_data, id, session)
    return update_client


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clients(
    id: UUID,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    RoleChecker.is_superuser(current_user.role)
    await service.delete_client(id, session)
    return "success"


@router.get("/count", response_model=CountClientDTO, status_code=status.HTTP_200_OK)
async def count_clients(
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    num_of_clients = await service.count_clients(session)
    return num_of_clients


# @router.post("/appointments", status_code=status.HTTP_201_CREATED, response_model=AppointmentReadDTO)
# async def create_appointment(
#     appointment_data: AppointmentCreateDTO,
#     service: ClientService = Depends(get_client_service),
#     session: AsyncSession = Depends(db_manager.get_async_session),
#     current_user: UserReadDTO = Depends(auth_service.get_current_user)
# ):
#     if await doctor_service.is_day_off(appointment_data.appointment_date, appointment_data.doctor_id,
#                                  session):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="The doctor is going to rest that day"
#         )
#     new_appointment = await service.create_appointment(appointment_data, session)
#     return new_appointment


@router.post("/mail_delivery", status_code=201)
async def mail_delivery(
    email_data: CreateMail,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    await service.mail_delivery(email_data, session)


@router.get("/search/{fullname}", response_model=list[SearchClientDTO])
async def search_by_fio(
    fullname: str,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    clients = await service.search_client_by_fio(fullname, session)
    return clients