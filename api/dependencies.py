from api.repositories.appointments import AppointmentsRepository
from api.repositories.client import ClientRepository
from api.repositories.doctor import DoctorRepository
from api.repositories.user import UserRepository
from api.services.appointments import AppointmentsService
from api.services.auth import AuthService
from api.services.client import ClientService
from api.services.doctor import DoctorService
from api.services.user import UserService


user_repo = UserRepository()
doctor_repo = DoctorRepository()
client_repo = ClientRepository()
appointments_repo = AppointmentsRepository()

client_service = ClientService(client_repo)
user_service = UserService(user_repo)
auth_service = AuthService(user_repo)
doctor_service = DoctorService(doctor_repo)
appointments_service = AppointmentsService(appointments_repo)


def get_user_service() -> UserService:
    return user_service


def get_auth_service() -> AuthService:
    return auth_service


def get_doctor_service() -> DoctorService:
    return doctor_service


def get_client_service() -> ClientService:
    return client_service


def get_appointments_service() -> AppointmentsService:
    return appointments_service
