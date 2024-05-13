from api.models.base import Base
import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text, ForeignKey

class AppointmentModel(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[UUID] = mapped_column(ForeignKey('doctors.id', ondelete='CASCADE'))
    client_id: Mapped[UUID] = mapped_column(ForeignKey('clients.id', ondelete='CASCADE'))
    appointment_date: Mapped[datetime.datetime]
    