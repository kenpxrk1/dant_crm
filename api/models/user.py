import enum
from api.models.base import Base
import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text


class UserRole(str, enum.Enum):
    admin = 'admin'
    super_user = 'super_user'

    


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    role: Mapped[UserRole] = mapped_column(default="admin")
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    

