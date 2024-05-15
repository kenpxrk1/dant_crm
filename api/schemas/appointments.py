from pydantic import BaseModel
from uuid import UUID
import datetime


class AppointmentBaseSchema(BaseModel):
    doctor_id: UUID
    client_id: UUID
    appointment_date: datetime.date
    appointment_time: datetime.time


class AppointmentCreateDTO(AppointmentBaseSchema):
    pass 


class AppointmentUpdateDTO(AppointmentCreateDTO):
    pass


class AppointmentReadDTO(AppointmentBaseSchema):
    id: int