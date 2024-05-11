from fastapi import HTTPException, status
from api.repositories.user import UserRepository
from api.schemas.user import UserCreateDTO, UserReadDTO
from api.utils.hasher import HashingMixin

class UserService():
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    
    async def create_user(self, user_data: UserCreateDTO, session) -> UserReadDTO:
        user_data = user_data.model_dump() 
        print(user_data)
        user_data["password"] = HashingMixin.hasher(user_data["password"])
        user = await self.repo.add_one(user_data, session)
        return UserReadDTO.model_validate(user, from_attributes=True)

    async def get_users(self, session) -> list[UserReadDTO]:
        users = await self.repo.find_all(session)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='users not found'
            )
        return [UserReadDTO.model_validate(user, from_attributes=True) for user in users]
        
