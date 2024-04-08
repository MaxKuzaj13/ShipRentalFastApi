from pydantic import BaseModel, PositiveInt, root_validator
from typing import Optional
from datetime import datetime


class BookingsSchema(BaseModel):
    id: Optional[PositiveInt]
    spaceship_id: PositiveInt
    customer_id: PositiveInt
    date_start: datetime
    date_end: datetime

    @root_validator(skip_on_failure=True)
    def validate_dates(cls, values):
        """
        root_validator is needed to check all model not single field
        :param values: object
        :return: values: object
        """
        if values.get('date_end') < values.get('date_start'):
            raise ValueError('date_end should be greater then date_start')
        return values
