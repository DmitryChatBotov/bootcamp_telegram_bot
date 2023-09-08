from pydantic import BaseModel


class Reservation(BaseModel):
    master: str | None = None
    beauty_procedure: str
    date: str
    time: str
    price: float
    duration: int
