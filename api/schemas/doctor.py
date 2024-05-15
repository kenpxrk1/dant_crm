import re
from uuid import UUID
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

RUSSIAN_ALPHABET_SYMBOLS = re.compile(r"^[а-яА-Яa\- ]+$")


class DoctorBaseSchema(BaseModel):
    fullname: str
    occupation: str
    phone_number: PhoneNumber

    @field_validator('fullname', 'occupation')
    def russian_symbols_validator(value):
        """ checks that value consist only
         russian, line, space symbols 
        """
        if not RUSSIAN_ALPHABET_SYMBOLS.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Имя должно состоять из русских букв",
            )
        return value


class DoctorCreateDTO(DoctorBaseSchema):
    pass 

class DoctorUpdateDTO(DoctorBaseSchema):
    pass

class DoctorReadDTO(DoctorBaseSchema):
    id: UUID
    vacation: bool | None


class CountDoctorDTO(BaseModel):
    doctors_num: int
