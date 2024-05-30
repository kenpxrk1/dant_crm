from .user import router as user_router
from .doctor import router as doctor_router
from .client import router as client_router
from .appointments import router as appointments_router


routers = [user_router, doctor_router, client_router, appointments_router]
