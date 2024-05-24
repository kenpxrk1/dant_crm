from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.handlers.routers import routers
from api.dependencies import user_service, user_repo
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await db_manager.create_table()
    await user_service.create_super_user()
    yield


app = FastAPI(title="CRM DANTIST", lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)
