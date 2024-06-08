import re
from uuid import UUID
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from api.schemas.client import check_other_symbols

RUSSIAN_ALPHABET_SYMBOLS = re.compile(r"^[а-яА-Яa\- ]+$")


class DoctorBaseSchema(BaseModel):
    fullname: str
    occupation: str
    phone_number: PhoneNumber

    @field_validator('fullname')
    def not_empty_validator(value):
        if value == '' or value == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя не должно быть пустой строкой"
            )
        if value.isspace():
            raise HTTPException(
                status_code=400,
                detail="Имя не должно состоять только из пробелов"
            )
        if check_other_symbols(value):
            return value
        else:
            raise HTTPException(
                status_code=400,
                detail="Введите корректное имя"
            )

    @field_validator("fullname", "occupation")
    def russian_symbols_validator(value):
        """checks that value consist only
        russian, line, space symbols
        """
        if not RUSSIAN_ALPHABET_SYMBOLS.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Имя должно состоять из русских букв",
            )
        return value

    @field_validator(
        "phone_number"
    )  # class PhoneNumber adding <tel:> symbols before user input. This method cuts them
    def cut_tel_symbols(value):
        return str(value)[4:]


class DoctorCreateDTO(DoctorBaseSchema):
    pass


class DoctorUpdateDTO(DoctorBaseSchema):
    pass


class DoctorReadDTO(DoctorBaseSchema):
    id: UUID
    vacation: bool | None


class CountDoctorDTO(BaseModel):
    doctors_num: int


class SearchDoctorDTO(BaseModel):
    id: UUID
    fullname: str
    