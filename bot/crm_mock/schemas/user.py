from pydantic import BaseModel


class User(BaseModel):
    id: int
    phone: str
    name: str
