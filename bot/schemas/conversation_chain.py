from pydantic import BaseModel


class Booking(BaseModel):
    action: str
    master_name: str | None = None
    beauty_service: str | None = None
    booking_date: str
    booking_time: str | None = None


class ChatMessage(BaseModel):
    text: str
