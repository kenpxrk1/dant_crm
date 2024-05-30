import datetime
from uuid import UUID
from fastapi import HTTPException, status
from api.repositories.client import ClientRepository
from api.schemas.client import (
    ClientCreateDTO,
    ClientReadDTO,
    ClientUpdateDTO,
    CountClientDTO,
    SearchClientDTO,
)
from api.schemas.appointments import AppointmentReadDTO, AppointmentCreateDTO
from api.schemas.mail import CreateMail
from api.tasks.tasks import send_mail


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
                status_code=status.HTTP_404_NOT_FOUND, detail="clients not found"
            )
        return [
            ClientReadDTO.model_validate(client, from_attributes=True)
            for client in clients
        ]

    async def update_doctor(
        self, client_data: ClientUpdateDTO, id: UUID, session
    ) -> ClientReadDTO:
        client_data = client_data.model_dump()
        updated_client = await self.repo.update_one(client_data, id, session)
        if updated_client == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="client not found"
            )
        return ClientReadDTO.model_validate(updated_client, from_attributes=True)

    async def delete_client(self, id: UUID, session) -> None:
        await self.repo.delete_one(id, session)

    async def count_clients(self, session) -> CountClientDTO:
        num_of_clients = await self.repo.count_all(session)
        return CountClientDTO(num_of_clients=num_of_clients)

    # async def create_appointment(self, appointment_data: AppointmentCreateDTO, session) -> AppointmentReadDTO:
    #     appointment_data = appointment_data.model_dump()
    #     new_appmnt = await self.repo.create_appointment(appointment_data, session)
    #     return AppointmentReadDTO.model_validate(new_appmnt, from_attributes=True)

    async def get_client_email(self, session):
        clients = await self.repo.find_all(session)
        mails_lst = []
        for client in clients:
            mails_lst.append(client.email)
        return mails_lst

    async def mail_delivery(self, mail_data: CreateMail, session) -> None:
        client_mails = await self.get_client_email(session)
        for mail in client_mails:
            try:

                send_mail.delay(
                    email=mail, title=mail_data.title, content=mail_data.content
                )
            except:
                continue
    
    async def search_client_by_fio(self, fullname: str, session) -> list[SearchClientDTO]:
        tuple_clients = await self.repo.search_by_fio(fullname, session)
        return [
            SearchClientDTO.model_validate(client, from_attributes=True)
            for client in tuple_clients
        ]