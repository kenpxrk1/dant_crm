from api.models.doctors import DoctorModel
from .repository import SQLAlchemyRepository

class DoctorRepository(SQLAlchemyRepository):
    
    model = DoctorModel