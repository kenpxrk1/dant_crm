from pydantic import BaseModel, field_validator
from uuid import UUID
import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber


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


class JoinedAppointmentsDTO(BaseModel):
    id: int
    client_name: str
    client_birthday: datetime.date
    client_phone: PhoneNumber
    doctor_name: str
    doctor_phone: PhoneNumber
    appointment_date: datetime.date
    appointment_time: datetime.time


class AppointmentsByOccupation(BaseModel):
    occupation: str
    appointments_counter: int


class AppointmentsByConditionInput(BaseModel):
    period_from: datetime.date
    period_to: datetime.date
