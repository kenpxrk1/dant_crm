from uuid import UUID
from fastapi import HTTPException, status
from api.repositories.user import UserRepository
from api.schemas.user import UserCreateDTO, UserReadDTO, UserUpdateDTO
from api.schemas.appointments import JoinedAppointmentsDTO
from api.utils.hasher import HashingMixin
from api.config import super_user


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def create_super_user(
        self, user_data: dict = super_user.super_user_data
    ) -> None:
        user_data["password"] = HashingMixin.hasher(user_data["password"])
        await self.repo.create_super_user(user_data)

    async def create_user(self, user_data: UserCreateDTO, session) -> UserReadDTO:
        user_data = user_data.model_dump()
        user_data["password"] = HashingMixin.hasher(user_data["password"])
        user = await self.repo.add_one(user_data, session)
        return UserReadDTO.model_validate(user, from_attributes=True)

    async def get_users(self, session) -> list[UserReadDTO]:
        users = await self.repo.find_all(session)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="users not found"
            )
        return [
            UserReadDTO.model_validate(user, from_attributes=True) for user in users
        ]

    async def update_user(
        self, user_data: UserUpdateDTO, id: UUID, session
    ) -> UserReadDTO:
        user_data = user_data.model_dump()
        new_user = await self.repo.update_one(user_data, id, session)
        if new_user == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )
        return UserReadDTO.model_validate(new_user, from_attributes=True)

    async def delete_user(self, id: UUID, session) -> None:
        await self.repo.delete_one(id, session)

    async def get_appointments(self, session) -> list[JoinedAppointmentsDTO]:
        appointments = await self.repo.get_appointments(session)
        print(appointments)
        return [
            JoinedAppointmentsDTO.model_validate(appointment, from_attributes=True)
            for appointment in appointments
        ]
