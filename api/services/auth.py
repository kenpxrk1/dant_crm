import datetime
from api.db import db_manager
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.repositories.user import UserRepository
from jose import jwt, JWTError
from api.schemas.auth import TokenData
from api.config import auth_config
from api.schemas.user import UserReadDTO


class AuthService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

    def __init__(self, repository: UserRepository) -> None:
        self.repo = repository

    def create_access_token(
        self, data: dict, expires_delta: datetime.timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                minutes=15
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM
        )
        return encoded_jwt

    async def verify_access_token(self, token: str, form_data_exception):

        try:
            payload = jwt.decode(
                token, auth_config.SECRET_KEY, algorithms=auth_config.ALGORITHM
            )
            id: str = payload.get("id")
            if id is None:
                raise form_data_exception

            token_data = TokenData(id=id)

        except JWTError:
            raise form_data_exception

        return token_data

    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        session=Depends(db_manager.get_async_session),
    ):
        form_data_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not valid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = await self.verify_access_token(token, form_data_exception)
        print(token.id)
        user = await self.repo.find_one(token.id, session)
        return UserReadDTO.model_validate(user, from_attributes=True)

    async def authenticate_user(self, username, password, session):
        user = await self.repo.authenticate(username, password, session)
        return user
