from pydantic import BaseModel, PositiveInt, PositiveFloat, Field


class SpaceshipSchemaReceived(BaseModel):
    name: str = Field(min_length=5, max_length=255)
    price_per_hour: PositiveFloat
    available: bool
    max_speed: PositiveInt
    max_range: PositiveInt

    class Config:
        from_attributes = True


class SpaceshipSchemaStored(BaseModel):
    id: PositiveInt
    name: str = Field(min_length=5, max_length=255)
    price_per_hour: PositiveFloat
    available: bool
    max_speed: PositiveInt
    max_range: PositiveInt

    class Config:
        from_attributes = True
