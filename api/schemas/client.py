import datetime
import re
from uuid import UUID
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


RUSSIAN_ALPHABET_SYMBOLS = re.compile(r"^[а-яА-Яa\- ]+$")

def check_other_symbols(value: str) -> bool:
    counter = 0
    for char in value:
        if not (char.isalpha() or char.isspace() or '-'):
            return False
        if char.isalpha():
            counter += 1
    if counter == 0:
        return False
    else:
        return True



class ClientBaseSchema(BaseModel):
    fullname: str
    date_of_birth: datetime.date
    email: EmailStr
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
    
    @field_validator('date_of_birth')
    def date_of_birth_validator(value: datetime.date):

        """ Проверка корректности полученой даты рождения """

        current_date =  datetime.date.today()
        if value > current_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата рождения не может быть позже чем текущая дата."
            )
        if abs(int(current_date.year) - int(value.year)) >= 115: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недопустимая дата рождения"
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


class SearchClientDTO(BaseModel):
    id: UUID 
    fullname: str 
    date_of_birth: datetime.date

    @field_validator('date_of_birth')
    def date_of_birth_validator(value: datetime.date):

        """ Проверка корректности полученой даты рождения """

        current_date =  datetime.date.today()
        if value > current_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Дата рождения не может быть позже чем текущая дата."
            )
        if abs(current_date.year - value.year) >= 115: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Недопустимая дата рождения"
            )
        return value