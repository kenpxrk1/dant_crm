from uuid import uuid4
import pytest
import datetime as dt
from httpx import AsyncClient
from tests.conftest import create_test_auth_headers_for_user
from api.utils.hasher import HashingMixin


@pytest.mark.asyncio
async def test_create_doctor(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors):
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
    doctor_data = {
    "fullname": "Олег Игоревич Самолетов",
    "occupation": "Ортодонт",
    "phone_number": "+79158224123"
    }
    resp = await ac.post('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=doctor_data)
    assert resp.status_code == 201
    doctors = await get_doctors()
    assert len(doctors) == 1
    await clean_tables()

@pytest.mark.asyncio
async def test_create_doctors_empty_fio(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors, get_users):
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
    
    doctor_data = {
    "fullname": "doctor",
    "occupation": "Ортодонт",
    "phone_number": "+79158224123"
    }
    resp = await ac.post('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=doctor_data)
    assert resp.status_code == 422
    assert resp.json()['detail'] == 'Имя должно состоять из русских букв'
    doctors = await get_doctors()
    assert len(doctors) == 0
    await clean_tables()




    


    