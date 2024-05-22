from datetime import timedelta
import datetime
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas.auth import Token
from api.schemas.user import UserCreateDTO, UserReadDTO, UserUpdateDTO
from api.schemas.appointments import JoinedAppointmentsDTO, AppointmentsByOccupation, AppointmentsByConditionInput
from api.dependencies import get_auth_service, get_user_service, auth_service, doctor_service
from api.services.auth import AuthService
from api.services.user import UserService
from api.db import db_manager
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.role_checker import RoleChecker


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserReadDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDTO,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    RoleChecker.is_superuser(current_user.role)
    user = await service.create_user(user_data, session)
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_manager.get_async_session)
):
    user = await service.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    token = service.create_access_token(
        data=({"id": str(user.id), "role": user.role}),
        expires_delta=timedelta(minutes=60 * 8),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("", response_model=list[UserReadDTO])
async def get_users(
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    users = await service.get_users(session)
    return users

@router.put("/{id}", response_model=UserReadDTO, status_code=status.HTTP_201_CREATED)
async def update_user(
    user_data: UserUpdateDTO,
    id: UUID,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):  
    RoleChecker.is_superuser(current_user.role)
    updated_user = await service.update_user(user_data, id, session)
    return updated_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: UUID,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):  
    RoleChecker.is_superuser(current_user.role)
    await service.delete_user(id, session)


@router.get("/appointments", status_code=status.HTTP_201_CREATED, response_model=list[JoinedAppointmentsDTO])
async def get_appointments(
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
): 
    appointments = await service.get_appointments(session)
    return appointments


@router.get("/appointments/report/occupation/}", status_code=status.HTTP_201_CREATED, response_model=list[AppointmentsByOccupation])
async def get_appointments_stats_for_doctors_by_occupation(
    date_from: datetime.date,
    date_to: datetime.date,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    request_data = AppointmentsByConditionInput(
        period_from=date_from,
        period_to=date_to
    )
    appointments = await service.get_appointments_stats_for_doctors_by_occupation(request_data, session)
    return appointments