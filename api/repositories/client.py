from api.models.client import ClientModel
from api.repositories.repository import SQLAlchemyRepository


class ClientRepository(SQLAlchemyRepository):
    
    model = ClientModel