from api.models.doctor import DoctorModel
from .repository import SQLAlchemyRepository

class DoctorRepository(SQLAlchemyRepository):
    
    model = DoctorModel