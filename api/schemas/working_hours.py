from pydantic import BaseModel
from uuid import UUID
import datetime as dt
from api.models.working_hours import WeekDay


class WorkingHours(BaseModel):
    doctor_id: UUID
    day_of_week: WeekDay
    start_time: dt.time | None
    end_time: dt.time | None