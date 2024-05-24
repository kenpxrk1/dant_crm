import datetime
from uuid import UUID
from .repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db_manager
from sqlalchemy.orm import aliased
from sqlalchemy import ScalarResult, desc, func, insert, select, update, delete, join
from api.models.user import UserModel
from api.models.client import ClientModel
from api.models.appointments import AppointmentModel
from api.models.doctor import DoctorModel
from api.utils.hasher import HashingMixin
from sqlalchemy.exc import IntegrityError


class UserRepository(SQLAlchemyRepository):

    model = UserModel

    async def create_super_user(self, user_data: dict) -> None:
        async with db_manager.async_session() as session:
            try:
                super_user_query = select(self.model).where(
                    user_data["login"] == self.model.login
                )
                user = await session.execute(super_user_query)
                if user.scalar_one_or_none() == None:
                    super_user_insert = insert(self.model).values(**user_data)
                    await session.execute(super_user_insert)
                    await session.commit()
            except IntegrityError:
                pass

    async def authenticate(
        self, username, password, session: AsyncSession
    ) -> ScalarResult | None:
        stmt = select(self.model).where(username == self.model.login)
        user = await session.execute(stmt)
        user = user.scalars().first()

        if not user:
            return None
        if HashingMixin.verify(hashed_password=user.password, plain_password=password):
            return user
        else:
            return None

