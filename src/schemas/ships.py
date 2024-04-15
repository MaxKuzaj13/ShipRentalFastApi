from pydantic import BaseModel, PositiveInt, PositiveFloat, Field


class SpaceshipSchemaReceived(BaseModel):
    name: str = Field(min_length=5, max_length=255)
    price_per_hour: PositiveFloat
    available: bool
    max_speed: PositiveInt
    max_range: PositiveInt

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "B-wing",
                "price_per_hour": 600.0,
                "available": True,
                "max_speed": 900,
                "max_range": 250
            }

        }


class SpaceshipSchemaStored(BaseModel):
    id: PositiveInt
    name: str = Field(min_length=5, max_length=255)
    price_per_hour: PositiveFloat
    available: bool
    max_speed: PositiveInt
    max_range: PositiveInt

    class Config:
        from_attributes = True

        class Config:
            from_attributes = True
            json_schema_extra = {
                "example": {
                    "id":12,
                    "name": "B-wing",
                    "price_per_hour": 600.0,
                    "available": True,
                    "max_speed": 900,
                    "max_range": 250
                }

            }
