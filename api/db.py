from typing import AsyncGenerator
from sqlalchemy import Index
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from api.config import db_settings
from api.models.base import Base
from api.models.days_off import DayOffModel

class DBManager():
    def __init__(self):
        self.async_engine = create_async_engine(
            url=db_settings.DATABASE_URL,
            echo=True,
        )
        self.async_session = async_sessionmaker(self.async_engine, class_=AsyncSession, expire_on_commit=False)
    
    async def get_async_session(self) -> AsyncGenerator:
        async with self.async_session() as session:
            yield session
    
    async def create_table(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            
            
            

db_manager = DBManager()


