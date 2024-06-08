from fastapi import HTTPException
from api.models.base import Base
import datetime as dt
import enum
from uuid import UUID, uuid4
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text, ForeignKey, UniqueConstraint


class WeekDay(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    def get_weekday_by_number(number):
        try:
            wd_object = WeekDay(number)
            return wd_object.name
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Такой день недели не существует"
            )


class WorkingHoursModel(Base):
    __tablename__ = "working_hours"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[UUID] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE"),
        )
    day_of_week: Mapped[WeekDay]
    start_time: Mapped[dt.time] = mapped_column(default=dt.time(8, 0))
    end_time: Mapped[dt.time] = mapped_column(default=dt.time(20, 0))
