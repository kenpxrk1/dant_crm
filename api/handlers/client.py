from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.dependencies import get_client_service, ClientService, auth_service
from api.schemas.client import ClientCreateDTO, ClientReadDTO, ClientUpdateDTO, CountClientDTO
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db_manager
from api.schemas.user import UserReadDTO
from api.utils.role_checker import RoleChecker
from api.schemas.appointments import AppointmentCreateDTO, AppointmentReadDTO


router = APIRouter(prefix="/clients", tags=["Client"])


@router.post("", response_model=ClientReadDTO, status_code=status.HTTP_201_CREATED)
async def add_new_client(
    client_data: ClientCreateDTO,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    new_doctor = await service.add_client(client_data, session)
    return new_doctor


@router.get("", response_model=list[ClientReadDTO], status_code=status.HTTP_200_OK)
async def get_clients(
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    clients = await service.get_clients(session)
    return clients


@router.put("/{id}", response_model=ClientReadDTO, status_code=status.HTTP_201_CREATED)
async def update_clients(
    client_data: ClientUpdateDTO,
    id: UUID,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    update_client = await service.update_doctor(client_data, id, session)
    return update_client

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clients(
    id: UUID,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    RoleChecker.is_superuser(current_user.role)
    await service.delete_client(id, session)
    return "success"


@router.get("/count", response_model=CountClientDTO, status_code=status.HTTP_200_OK)
async def count_clients(
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    num_of_clients = await service.count_clients(session)
    return num_of_clients


@router.post("/appointments", status_code=status.HTTP_201_CREATED, response_model=AppointmentReadDTO)
async def create_appointment(
    appointment_data: AppointmentCreateDTO,
    service: ClientService = Depends(get_client_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    new_appointment = await service.create_appointment(appointment_data, session)
    return new_appointment