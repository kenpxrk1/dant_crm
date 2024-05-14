from pydantic import BaseModel
from uuid import UUID
import datetime


class CreateDaysOffDTO(BaseModel):
    days_off_date: list[datetime.date]


class ReadDaysOffDTO(CreateDaysOffDTO):
    doctor_id: int | UUID