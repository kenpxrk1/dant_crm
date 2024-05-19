from pydantic import BaseModel


class CreateMail(BaseModel):
    title: str
    content: str