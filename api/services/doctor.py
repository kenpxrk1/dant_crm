import datetime
from uuid import UUID
from fastapi import HTTPException, status
from api.schemas.doctor import DoctorCreateDTO, DoctorReadDTO, DoctorUpdateDTO, SearchDoctorDTO
from api.repositories.doctor import DoctorRepository
from api.schemas.doctor import CountDoctorDTO
from api.schemas.working_hours import WorkingHours

class DoctorService:
    def __init__(self, repo: DoctorRepository):
        self.repo = repo

    async def add_doctor(self, doctor_data: DoctorCreateDTO, session) -> DoctorReadDTO:
        doctor_data = doctor_data.model_dump()
        doctor = await self.repo.add_one(doctor_data, session)
        return DoctorReadDTO.model_validate(doctor, from_attributes=True)

    async def get_doctors(self, session) -> list[DoctorReadDTO]:
        doctors = await self.repo.find_all(session)
        if not doctors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="doctors not found"
            )
        return [
            DoctorReadDTO.model_validate(doctor, from_attributes=True)
            for doctor in doctors
        ]

    async def update_doctor(
        self, doctor_data: DoctorUpdateDTO, id: UUID, session
    ) -> DoctorReadDTO:
        doctor_data = doctor_data.model_dump()
        new_doctor_data = await self.repo.update_one(doctor_data, id, session)
        if new_doctor_data == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="doctor not found"
            )
        return DoctorReadDTO.model_validate(new_doctor_data)

    async def delete_doctor(self, id: UUID, session) -> None:
        await self.repo.delete_one(id, session)

    async def count_doctors(self, session) -> CountDoctorDTO:
        doctors_num = await self.repo.count_all(session)
        return CountDoctorDTO(doctors_num=doctors_num)

    async def search_doctor_by_fio(self, fullname: str, session) -> list[SearchDoctorDTO]:
        tuple_doctors = await self.repo.search_by_fio(fullname, session)
        return [
            SearchDoctorDTO.model_validate(tuple_doctor, from_attributes=True)
            for tuple_doctor in tuple_doctors
        ]
    
    async def create_working_hours(self, data: WorkingHours, session):
        wh_data = data.model_dump()
        new_wh = await self.repo.create_working_hours(wh_data, session)
        return WorkingHours.model_validate(new_wh, from_attributes=True)