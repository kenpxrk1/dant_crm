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


class WorkingHoursModel(Base):
    __tablename__ = "working_hours"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[UUID] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE")
        )
    day_of_week: Mapped[WeekDay]
    start_time: Mapped[dt.time] = mapped_column(default=dt.time(8, 0))
    end_time: Mapped[dt.time] = mapped_column(default=dt.time(20, 0))
