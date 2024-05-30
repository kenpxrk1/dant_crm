import re
from uuid import UUID
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from api.models.user import UserRole

RUSSIAN_ALPHABET_SYMBOLS = re.compile(r"^[а-яА-Яa\-]+$")


class UserBase(BaseModel):
    login: EmailStr
    name: str
    surname: str

    @field_validator("name", "surname")
    def russian_symbols_validator(value):
        """checks that value consist only russian letters
        and line
        """

        if not RUSSIAN_ALPHABET_SYMBOLS.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Имя должно состоять из русских букв",
            )
        return value


class UserCreateDTO(UserBase):
    password: str


class UserUpdateDTO(UserBase):
    role: UserRole


class UserReadDTO(UserBase):
    id: UUID
    role: UserRole
