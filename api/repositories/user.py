from uuid import UUID
from .repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db_manager
from sqlalchemy import ScalarResult, insert, select, update, delete
from api.models.user import UserModel
from api.utils.hasher import HashingMixin
from sqlalchemy.exc import IntegrityError


class UserRepository(SQLAlchemyRepository):

    model = UserModel

    async def create_super_user(self, user_data: dict) -> None:
        async with db_manager.async_session() as session:
            try:
                super_user_query = select(self.model).where(user_data["login"] == self.model.login)
                user = await session.execute(super_user_query)
                if user.scalar_one_or_none() == None:
                    super_user_insert = insert(self.model).values(**user_data)
                    await session.execute(super_user_insert)
                    await session.commit()
            except IntegrityError:
                pass


    # async def add_one(self, user_data: dict, session: AsyncSession) -> ScalarResult:
    #     insert_user_query = insert(UserModel).values(**user_data).returning(UserModel)
    #     user = await session.execute(insert_user_query)
    #     await session.commit()
    #     return user.scalar_one()

    # async def find_all(self, session: AsyncSession) -> ScalarResult | None:
    #     users_query = select(UserModel)
    #     users = await session.execute(users_query)
    #     users = users.scalars().all()
    #     if users == None:
    #         return None
    #     return users

    # async def find_one(self, id: UUID, session: AsyncSession) -> ScalarResult | None:
    #     user_query = select(UserModel).where(UserModel.id == id)
    #     user = await session.execute(user_query)
    #     return user.scalar_one_or_none()

    # async def update_one(self, user_data: dict, id: UUID, session: AsyncSession) -> ScalarResult | None:
    #     update_user_query = (
    #         update(UserModel)
    #         .where(UserModel.id == id)
    #         .values(**user_data)
    #         .returning(UserModel)
    #     )
    #     updated_user = await session.execute(update_user_query)
    #     # await session.refresh(UserModel)
    #     await session.commit()
    #     return updated_user.scalar_one_or_none()

    # async def delete_one(self, id: UUID, session: AsyncSession) -> None:
    #     delete_user_query = delete(UserModel).where(UserModel.id == id)
    #     await session.execute(delete_user_query)
    #     await session.commit()

    async def authenticate(self, username, password, session: AsyncSession) -> ScalarResult | None:
        stmt = select(self.model).where(username == self.model.login)
        user = await session.execute(stmt)
        user = user.scalars().first()

        if not user:
            return None
        if HashingMixin.verify(hashed_password=user.password, plain_password=password):
            return user
        else: 
            return None