from uuid import UUID
from fastapi import HTTPException, status
from api.schemas.doctor import DoctorCreateDTO, DoctorReadDTO, DoctorUpdateDTO
from api.repositories.doctor import DoctorRepository


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
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='doctors not found'
            )
        return [DoctorReadDTO.model_validate(doctor, from_attributes=True) for doctor in doctors]
    
    async def update_doctor(self, doctor_data: DoctorUpdateDTO, id: UUID, session) -> DoctorReadDTO:
        doctor_data = doctor_data.model_dump()
        new_doctor_data = await self.repo.update_one(doctor_data, id, session)
        if new_doctor_data == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='doctor not found'
            )
        return DoctorReadDTO.model_validate(new_doctor_data)
    
    async def delete_doctor(self, id: UUID, session) -> None:
        await self.repo.delete_one(id, session)
        