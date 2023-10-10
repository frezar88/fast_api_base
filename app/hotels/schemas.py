from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    rooms_quantity: int
    services: list
    image_id: int

