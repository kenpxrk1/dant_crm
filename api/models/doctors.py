from api.models.base import Base
import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text


class DoctorModel(Base):
    __tablename__ = "doctors"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    fullname: Mapped[str]
    occupation: Mapped[str]
    vacation: Mapped[bool | None]
    phone_number: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
