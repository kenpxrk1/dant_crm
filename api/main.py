from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.db import db_manager
from api.handlers.routers import routers
from api.dependencies import user_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.create_table()
    await user_service.create_super_user()
    yield


app = FastAPI(
    title="CRM DANTIST",
    lifespan=lifespan
)

for router in routers:
    app.include_router(router)