from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(BaseModel):
    user_id: int
    phone: str
    name: str
