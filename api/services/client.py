import datetime
from uuid import UUID
from fastapi import HTTPException, status
from api.repositories.client import ClientRepository
from api.schemas.client import ClientCreateDTO, ClientReadDTO, ClientUpdateDTO, CountClientDTO
from api.schemas.appointments import AppointmentReadDTO, AppointmentCreateDTO


class ClientService:
    def __init__(self, repo: ClientRepository):
        self.repo = repo
    

    async def add_client(self, client_data: ClientCreateDTO, session) -> ClientReadDTO:
        client_data = client_data.model_dump()
        client = await self.repo.add_one(client_data, session)
        return ClientReadDTO.model_validate(client, from_attributes=True)
    

    async def get_clients(self, session) -> list[ClientReadDTO]:
        clients = await self.repo.find_all(session)
        if not clients:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='clients not found'
            )
        return [ClientReadDTO.model_validate(client, from_attributes=True) for client in clients]
    

    async def update_doctor(self, client_data: ClientUpdateDTO, id: UUID, session) -> ClientReadDTO:
        client_data = client_data.model_dump()
        updated_client = await self.repo.update_one(client_data, id, session)
        if updated_client == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='client not found'
            )
        return ClientReadDTO.model_validate(updated_client, from_attributes=True)
    

    async def delete_client(self, id: UUID, session) -> None:
        await self.repo.delete_one(id, session)


    async def count_clients(self, session) -> CountClientDTO:
        num_of_clients = await self.repo.count_all(session)
        return CountClientDTO(
            num_of_clients=num_of_clients
        )


    async def create_appointment(self, appointment_data: AppointmentCreateDTO, session) -> AppointmentReadDTO:
        appointment_data = appointment_data.model_dump()
        new_appmnt = await self.repo.create_appointment(appointment_data, session)
        return AppointmentReadDTO.model_validate(new_appmnt, from_attributes=True)
