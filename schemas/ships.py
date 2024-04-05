from pydantic import BaseModel

class Starship(BaseModel):
    name: str
    price_per_hour: float
    available: bool