from api.models.base import Base
import datetime
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint

class AppointmentModel(Base):
    __tablename__ = "appointments"

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "appointment_date",
            name="idx_doctor_datetime_unique"
        ),
        UniqueConstraint(
            "client_id",
            "appointment_date",
            name="idx_client_datetime_unique"
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[UUID] = mapped_column(ForeignKey('doctors.id', ondelete='CASCADE'))
    client_id: Mapped[UUID] = mapped_column(ForeignKey('clients.id', ondelete='CASCADE'))
    appointment_date: Mapped[datetime.date]
    appointment_time: Mapped[datetime.time]
    