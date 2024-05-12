from api.repositories.doctor import DoctorRepository
from api.repositories.user import UserRepository 
from api.services.auth import AuthService
from api.services.doctor import DoctorService
from api.services.user import UserService



user_repo = UserRepository()
doctor_repo = DoctorRepository()


user_service = UserService(user_repo)
auth_service = AuthService(user_repo)
doctor_service = DoctorService(doctor_repo)


def get_user_service() -> UserService:
    return user_service


def get_auth_service() -> AuthService:
    return auth_service


def get_doctor_service() -> DoctorService:
    return doctor_service