from api.repositories.user import UserRepository 
from api.services.auth import AuthService
from api.services.user import UserService


user_repo = UserRepository()

user_service = UserService(user_repo)

auth_service = AuthService(user_repo)

def get_user_service() -> UserService:
    return user_service

def get_auth_service() -> AuthService:
    return auth_service