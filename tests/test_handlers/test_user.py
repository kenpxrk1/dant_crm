from uuid import uuid4
import pytest
import datetime as dt
from httpx import AsyncClient
from api.utils.hasher import HashingMixin
from tests.conftest import create_test_auth_headers_for_user


@pytest.mark.asyncio
async def test_create_superuser(create_user_in_database, get_users, get_user_from_database, clean_tables):
    user_data = {
        "id": uuid4(),
        "login": 'dagestan05@gmail.com',
        'password': '1234',
        'name': 'Magomed',
        'surname': 'aliev',
        'role': 'super_user',
        'created_at': dt.datetime.now()
    }
    await create_user_in_database(**user_data)
    users_from_db = await get_users()
    assert len(users_from_db) == 1
    user_from_db = await get_user_from_database(user_data["id"])
    assert len(user_from_db) == 1
    print(user_from_db)
    await clean_tables()

@pytest.mark.asyncio
async def test_login_superuser(ac: AsyncClient, create_user_in_database, clean_tables):
    user_data = {
        "id": uuid4(),
        "login": 'dagestan05@gmail.com',
        'password': HashingMixin.hasher('1234'),
        'name': 'Magomed',
        'surname': 'aliev',
        'role': 'super_user',
        'created_at': dt.datetime.now()
    }
    await create_user_in_database(**user_data)
    form_data = {
        "username": 'dagestan05@gmail.com',
        "password": '1234'
    }
    resp = await ac.post(f"users/login", data=form_data)
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp['access_token'] != None
    assert data_from_resp['token_type'] == 'bearer'
    await clean_tables()


@pytest.mark.asyncio
async def test_get_users_handler(ac: AsyncClient, create_user_in_database, clean_tables):
    user_data = {
        "id": uuid4(),
        "login": 'dagestan05@gmail.com',
        'password': HashingMixin.hasher('1234'),
        'name': 'Магомед',
        'surname': 'Алиев',
        'role': 'super_user',
        'created_at': dt.datetime.now()
    }
    await create_user_in_database(**user_data)
    print(create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    resp = await ac.get('/users', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    print(resp.json())
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    await clean_tables()


async def test_get_users_handler_401(ac: AsyncClient, clean_tables):
    token = 'fake-token-ne-ver-emu-servak'
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }
    resp = await ac.get('/users', headers=auth_headers)
    assert resp.status_code == 401 
    await clean_tables()

