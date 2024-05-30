import datetime
from uuid import UUID
from fastapi import HTTPException, status
from api.schemas.doctor import DoctorCreateDTO, DoctorReadDTO, DoctorUpdateDTO, SearchDoctorDTO
from api.repositories.doctor import DoctorRepository
from api.schemas.days_off import CreateDaysOffDTO, ReadDaysOffDTO
from api.schemas.doctor import CountDoctorDTO


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

    async def create_days_off(
        self, days_off_data: CreateDaysOffDTO, id: UUID, session
    ) -> ReadDaysOffDTO:
        days_off_data = days_off_data.model_dump()
        created_days_off = await self.repo.create_days_off(days_off_data, id, session)
        return ReadDaysOffDTO(days_off_date=created_days_off, doctor_id=id)

    async def is_day_off(self, date: datetime.date, id: UUID | int, session) -> bool:
        """
        Returns True, if date param is in doctors days_off,
        and False if its not in days_off.
        """
        days_off = await self.repo.get_days_off(date, id, session)
        print(days_off)
        if date in days_off:
            return True
        return False

    async def search_doctor_by_fio(self, fullname: str, session) -> list[SearchDoctorDTO]:
        tuple_doctors = await self.repo.search_by_fio(fullname, session)
        print(tuple_doctors)
        return [
            SearchDoctorDTO.model_validate(tuple_doctor, from_attributes=True)
            for tuple_doctor in tuple_doctors
        ]