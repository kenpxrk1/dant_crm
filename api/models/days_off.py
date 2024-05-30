from typing import List
from api.models.base import Base
import datetime
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Index, UniqueConstraint


class DayOffModel(Base):
    __tablename__ = "days_off"
    __table_args__ = (
        UniqueConstraint("doctor_id", "days_off_date", name="idx_unique_day_off"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doctor_id: Mapped[UUID] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE")
    )
    days_off_date: Mapped[datetime.date]
