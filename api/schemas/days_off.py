from pydantic import BaseModel
from uuid import UUID
import datetime


class CreateDaysOffDTO(BaseModel):
    doctor_id: UUID
    days_off_date: list[datetime.date]


class ReadDaysOffDTO(CreateDaysOffDTO):
    pass