from fastapi import HTTPException
from sqlalchemy import Integer, ScalarResult, func, insert, select
from api.models.client import ClientModel
from api.repositories.repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.appointments import AppointmentModel
from sqlalchemy.exc import IntegrityError


class ClientRepository(SQLAlchemyRepository):
    
    model = ClientModel
    

    