import datetime
from typing import AsyncGenerator
from uuid import UUID, uuid4
import asyncpg
from pydantic import EmailStr
from api.db import db_manager
from api.main import app
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import asyncio
import pytest
from api.config import test_db_settings
from api.models import Base
from api.utils.hasher import HashingMixin
from api.models.user import UserRole
from api.dependencies import auth_service


tables = ['users', 'doctors', 'clients']

async_engine = create_async_engine(test_db_settings.TEST_DATABASE_URL)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_init(event_loop):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(test_db_settings.TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    await pool.close()


@pytest.fixture
async def get_users(asyncpg_pool):
    async def get_users_from_db():
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM users""")

    return get_users_from_db


@pytest.fixture
async def get_doctors(asyncpg_pool):
    async def get_doctors_from_db():
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM doctors""")

    return get_doctors_from_db


@pytest.fixture
async def get_clients(asyncpg_pool):
    async def get_clients_from_db():
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM clients""")

    return get_clients_from_db


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(asyncpg_pool):
    async def clean_tables_from_db():
        async with asyncpg_pool.acquire() as conn:
            for table in tables:
                await conn.fetch(f"""DELETE FROM {table}""")
    return clean_tables_from_db

@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM users WHERE id = $1;""", user_id
            )

    return get_user_from_database_by_uuid


@pytest.fixture(scope='session')
async def create_doctor_in_database(asyncpg_pool):
    async def create_doctor_in_database(
        id: UUID,
        fullname: str,
        occupation: str,
        vacation: bool | None,
        phone_number: str,
        created_at: datetime.datetime
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO doctors VALUES ($1, $2, $3, $4, $5, $6)""",
                id,
                fullname,
                occupation,
                vacation,
                phone_number,
                created_at
            )

    return create_doctor_in_database


@pytest.fixture(scope='session')
async def create_client_in_database(asyncpg_pool):
    async def create_client_in_database(
        id: UUID,
        fullname: str,
        date_of_birth: datetime.date,
        email: str,
        phone_number: str,
        created_at: datetime.datetime
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO clients VALUES ($1, $2, $3, $4, $5, $6)""",
                id,
                fullname,
                date_of_birth,
                email,
                phone_number,
                created_at
            )

    return create_client_in_database


@pytest.fixture(scope='session')
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        id: UUID,
        login: EmailStr,
        password: str,
        name: str, 
        surname: str,
        role: str,
        created_at: datetime.datetime
        
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                id,
                login,
                password,
                name,
                surname,
                role,
                created_at,
            )

    return create_user_in_database



@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[db_manager.get_async_session] = get_test_session
        yield ac


@pytest.fixture(scope="session")
async def get_superuser_token(ac: AsyncClient, create_user_in_database):
    user_data = {
        "id": uuid4(),
        "login": 'dagestan05@gmail.com',
        'password': HashingMixin.hasher('1234'),
        'name': 'Магомед',
        'surname': 'Алиев',
        'role': UserRole.super_user,
        'created_at': datetime.datetime.now()
    }
    await create_user_in_database(**user_data)

    login_data = {
        'username': user_data['login'],
        'password': '1234'
    }

    resp = await ac.post('users/login', data=login_data)
    if resp.status_code == 200:
        return resp.json()['access_token']
    else:
        raise Exception

    
def create_test_auth_headers_for_user(id: str, role: str) -> dict[str, str]:
    access_token = auth_service.create_access_token(
        data=({"id": str(id), "role": role}),
        expires_delta=datetime.timedelta(minutes=60 * 8),
    )
    return {"Authorization": f"Bearer {access_token}"}