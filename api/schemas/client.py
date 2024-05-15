import datetime
import re
from uuid import UUID
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


RUSSIAN_ALPHABET_SYMBOLS = re.compile(r"^[а-яА-Яa\- ]+$")


class ClientBaseSchema(BaseModel):
    fullname: str
    date_of_birth: datetime.date
    email: EmailStr
    phone_number: PhoneNumber

    @field_validator('fullname')
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
    
    @field_validator('phone_number')
    def cut_tel_symbols(value):
        return str(value)[4:]
        


class ClientReadDTO(ClientBaseSchema):
    id: UUID
    created_at: datetime.datetime


class ClientCreateDTO(ClientBaseSchema):
    pass 


class ClientUpdateDTO(ClientCreateDTO):
    pass 


class CountClientDTO(BaseModel):
    num_of_clients: int
