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
async def test_create_doctors_eng_fio_error(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors, get_users):
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


@pytest.mark.asyncio
async def test_create_doctors_empty_fio_error(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors, get_users):
    user_data = {
        "id": uuid4(),
        "login": 'ivanov@gmail.com',
        'password': HashingMixin.hasher('1234'),
        'name': 'Иван',
        'surname': 'Иванов',
        'role': 'super_user',
        'created_at': dt.datetime.now()
    }
    await create_user_in_database(**user_data)
    
    doctor_data = {
    "fullname": "     ",
    "occupation": "Ортодонт",
    "phone_number": "+79158224123"
    }
    resp = await ac.post('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=doctor_data)
    assert resp.status_code == 400
    assert resp.json()['detail'] == 'Имя не должно состоять только из пробелов'
    doctors = await get_doctors()
    assert len(doctors) == 0

    await clean_tables()


@pytest.mark.asyncio
async def test_create_doctors_invalid_phone_error(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors, get_users):
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
    "fullname": "Олег Сергеевич Шапокляк",
    "occupation": "Ортодонт",
    "phone_number": "+7915822412"
    }
    resp = await ac.post('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=doctor_data)
    assert resp.status_code == 422
    doctors = await get_doctors()
    assert len(doctors) == 0

    doctor_data = {
    "fullname": "Олег Сергеевич Шапокляк",
    "occupation": "Ортодонт",
    "phone_number": "+791582241221212"
    }
    resp = await ac.post('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=doctor_data)

    assert resp.status_code == 422
    doctors = await get_doctors()
    assert len(doctors) == 0

    doctor_data = {
    "fullname": "Олег Сергеевич Шапокляк",
    "occupation": "Ортодонт",
    "phone_number": "+70008224425"
    }
    resp = await ac.post('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']), json=doctor_data)
    assert resp.status_code == 422
    doctors = await get_doctors()
    assert len(doctors) == 0
    await clean_tables()


@pytest.mark.asyncio
async def test_get_doctors(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors, create_doctor_in_database):
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
    "id": str(uuid4()),
    "fullname": "Олег Игоревич Самолетов",
    "occupation": "Ортодонт",
    "vacation": None,
    "phone_number": "+79158224123",
    "created_at": dt.datetime.now()
    }

    await create_doctor_in_database(**doctor_data)
    doctors = await get_doctors()
    assert len(doctors) == 1
    resp = await ac.get('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    await clean_tables()
    

@pytest.mark.asyncio
async def test_get_doctors_if_empty(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors):
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
    doctors = await get_doctors()
    assert len(doctors) == 0
    resp = await ac.get('/doctors', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    assert resp.status_code == 404
    await clean_tables()


@pytest.mark.asyncio
async def test_count_doctors(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors, create_doctor_in_database):
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


    doctor_data_1 = {
        "id": str(uuid4()),
        "fullname": "Олег Cергеевич Семак",
        "occupation": "Зубной",
        "vacation": None,
        "phone_number": "+79158224124",
        "created_at": dt.datetime.now()
    }

    doctor_data_2 = {
        "id": str(uuid4()),
        "fullname": "Олег Игоревич Самолетов",
        "occupation": "Ортодонт",
        "vacation": None,
        "phone_number": "+79158224123",
        "created_at": dt.datetime.now()
    }
    await create_doctor_in_database(**doctor_data_1)
    await create_doctor_in_database(**doctor_data_2)
    doctors = await get_doctors()
    assert len(doctors) == 2
    resp = await ac.get('/doctors/count', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    assert resp.status_code == 200
    assert resp.json()['doctors_num'] == 2
    await clean_tables()


@pytest.mark.asyncio
async def test_delete_doctor(ac: AsyncClient, create_user_in_database, clean_tables, get_doctors, create_doctor_in_database):
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


    doctor_data_1 = {
        "id": str(uuid4()),
        "fullname": "Олег Cергеевич Семак",
        "occupation": "Зубной",
        "vacation": None,
        "phone_number": "+79158224124",
        "created_at": dt.datetime.now()
    }
    await create_doctor_in_database(**doctor_data_1)
    resp = await ac.delete(f'/doctors/{doctor_data_1["id"]}', headers=create_test_auth_headers_for_user(user_data['id'], user_data['role']))
    assert resp.status_code == 204
    await clean_tables()

