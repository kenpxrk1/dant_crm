from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas.auth import Token, TokenData
from api.schemas.user import UserCreateDTO, UserReadDTO
from api.dependencies import get_auth_service, get_user_service, auth_service
from api.services.auth import AuthService
from api.services.user import UserService
from api.db import db_manager
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserReadDTO)
async def create_user(
    user_data: UserCreateDTO,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
):
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
        data=({"id": user.login, "role": user.role}),
        expires_delta=timedelta(minutes=60 * 8),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("", response_model=UserReadDTO)
async def get_users(
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: int = Depends(auth_service.get_current_user),
):
    users = await service.create_user(session)
    return users
