from pydantic import BaseModel, PositiveInt, root_validator
from datetime import datetime


class BookingsSchemaReceived(BaseModel):
    spaceship_id: PositiveInt
    customer_id: PositiveInt
    date_start: datetime
    date_end: datetime

    @root_validator(skip_on_failure=True)
    def validate_dates(cls, values):
        """
        Root validator to check the order of date_start and date_end.
        """
        date_start = values.get("date_start")
        date_end = values.get("date_end")
        if date_start and date_end and date_end < date_start:
            raise ValueError("date_end should be greater than or equal to date_start")
        return values

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "spaceship_id": 1,
                "customer_id": 2,
                "date_start": "2024-04-08T10:00:00",
                "date_end": "2024-04-09T10:00:00"
            }

        }


class BookingsSchemaStored(BaseModel):
    id: PositiveInt
    spaceship_id: PositiveInt
    customer_id: PositiveInt
    date_start: datetime
    date_end: datetime

    # Root validator skipped it is checked on receiving stage
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 12,
                "spaceship_id": 1,
                "customer_id": 2,
                "date_start": "2024-04-08T10:00:00",
                "date_end": "2024-04-09T10:00:00"
            }

        }
