from api.models.base import Base
import datetime as dt
import enum
from uuid import UUID, uuid4
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text, ForeignKey, UniqueConstraint


class DaysOffModel(Base):
    __tablename__ = "days_off"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id:Mapped[UUID] = mapped_column(ForeignKey("doctors.id", ondelete="CASCADE"))
    days_off_date: Mapped[dt.date] = mapped_column(nullable=False)