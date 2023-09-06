from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    phone: str
    name: str
