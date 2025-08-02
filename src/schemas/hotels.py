from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = None
    name: str | None = None