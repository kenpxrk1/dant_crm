from uuid import uuid4
import pytest
import datetime as dt
from httpx import AsyncClient
from tests.conftest import create_test_auth_headers_for_user
from api.utils.hasher import HashingMixin


@pytest.mark.asyncio
async def test_create_client(ac: AsyncClient, create_user_in_database, clean_tables, get_clients):
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
    client_data = {
        "fullname": "Иван Иванович Иванов",
        "date_of_birth": "2000-06-11",
        "email": "client@example.com",
        "phone_number": "+79001802512"
    }
    resp = await ac.post('/clients', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=client_data)
    assert resp.status_code == 201
    clients = await get_clients()
    assert len(clients) == 1
    await clean_tables()


@pytest.mark.asyncio
async def test_create_client_age_higher_than_current_date(ac: AsyncClient, create_user_in_database, clean_tables, get_clients):
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
    client_data = {
        "fullname": "Иван Иванович Иванов",
        "date_of_birth": "2025-06-11",
        "email": "client@example.com",
        "phone_number": "+79001802512"
    }
    resp = await ac.post('/clients', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=client_data)
    assert resp.status_code == 400
    assert resp.json()["detail"] == 'Дата рождения не может быть позже чем текущая дата.'
    clients = await get_clients()
    assert len(clients) == 0
    await clean_tables()


@pytest.mark.asyncio
async def test_create_client_age_higher_than_115(ac: AsyncClient, create_user_in_database, clean_tables, get_clients):
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
    client_data = {
        "fullname": "Иван Иванович Иванов",
        "date_of_birth": "1900-06-11",
        "email": "client@example.com",
        "phone_number": "+79001802512"
    }
    resp = await ac.post('/clients', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=client_data)
    assert resp.status_code == 400
    assert resp.json()["detail"] == 'Недопустимая дата рождения'
    clients = await get_clients()
    assert len(clients) == 0
    await clean_tables()


@pytest.mark.asyncio
async def test_incorrect_client_phone_number(ac: AsyncClient, create_user_in_database, clean_tables, get_clients):
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
    client_data = {
        "fullname": "Иван Иванович Иванов",
        "date_of_birth": "2000-06-11",
        "email": "client@example.com",
        "phone_number": "+7100200300"
    }
    resp = await ac.post('/clients', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=client_data)
    assert resp.status_code == 422
    clients = await get_clients()
    assert len(clients) == 0
    await clean_tables()


@pytest.mark.asyncio
async def test_get_clients(ac: AsyncClient, create_user_in_database, clean_tables, get_clients, create_client_in_database):
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
    client_data = {
        'id': str(uuid4()),
        'fullname': 'Андрей Викторович Жмышенко',
        'date_of_birth': dt.datetime.strptime('20040308', '%Y%m%d').date(),
        'email': 'vital@gmail.com',
        'phone_number': '+79001804561',
        'created_at': dt.datetime.now()
    }
    resp = await ac.get('/clients', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    assert resp.status_code == 404
    await create_client_in_database(**client_data)
    resp = await ac.get('/clients', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    await clean_tables() 


@pytest.mark.asyncio
async def test_delete_client(ac: AsyncClient, create_user_in_database, clean_tables, get_clients, create_client_in_database):
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
    client_data = {
        'id': str(uuid4()),
        'fullname': 'Андрей Викторович Жмышенко',
        'date_of_birth': dt.datetime.strptime('20040308', '%Y%m%d').date(),
        'email': 'vital@gmail.com',
        'phone_number': '+79001804561',
        'created_at': dt.datetime.now()
    }
    await create_client_in_database(**client_data)
    clients = await get_clients()
    assert len(clients) == 1
    resp = await ac.delete(f'/clients/{client_data["id"]}', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    assert resp.status_code == 204
    clients = await get_clients()
    assert len(clients) == 0
    await clean_tables()