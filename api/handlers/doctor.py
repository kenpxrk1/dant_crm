from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.dependencies import get_doctor_service, DoctorService, auth_service
from api.schemas.doctor import (
    CountDoctorDTO,
    DoctorReadDTO,
    DoctorCreateDTO,
    DoctorUpdateDTO,
    SearchDoctorDTO,
)
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db_manager
from api.schemas.user import UserReadDTO
from api.schemas.working_hours import WorkingHours



router = APIRouter(prefix="/doctors", tags=["Doctor"])


@router.post("", response_model=DoctorReadDTO, status_code=status.HTTP_201_CREATED)
async def add_new_doctor(
    doctor_data: DoctorCreateDTO,
    service: DoctorService = Depends(get_doctor_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    new_doctor = await service.add_doctor(doctor_data, session)
    return new_doctor


@router.get("", response_model=list[DoctorReadDTO], status_code=status.HTTP_200_OK)
async def get_doctors(
    service: DoctorService = Depends(get_doctor_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    doctors = await service.get_doctors(session)
    return doctors


@router.put("/{id}", response_model=DoctorReadDTO, status_code=status.HTTP_201_CREATED)
async def update_doctor(
    doctor_data: DoctorCreateDTO,
    id: UUID,
    service: DoctorService = Depends(get_doctor_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    update_doctor = await service.update_doctor(doctor_data, id, session)
    return update_doctor


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    id: UUID,
    service: DoctorService = Depends(get_doctor_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    await service.delete_doctor(id, session)
    return "success"


@router.get("/count", response_model=CountDoctorDTO, status_code=status.HTTP_200_OK)
async def count_doctors(
    service: DoctorService = Depends(get_doctor_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    doctors_num = await service.count_doctors(session)
    return doctors_num

@router.get("/search/{fullname}", response_model=list[SearchDoctorDTO])
async def search_by_fio(
    fullname: str,
    service: DoctorService = Depends(get_doctor_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user),
):
    doctors = await service.search_doctor_by_fio(fullname, session)
    return doctors


@router.post("/working-hours", response_model=WorkingHours)
async def create_working_hours(
    wh_data: WorkingHours,
    service: DoctorService = Depends(get_doctor_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: UserReadDTO = Depends(auth_service.get_current_user)
):
    new_wh = await service.create_working_hours(wh_data, session)
    return new_wh