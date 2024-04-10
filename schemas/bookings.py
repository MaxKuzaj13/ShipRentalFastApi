from pydantic import BaseModel, PositiveInt, root_validator
from datetime import datetime
def validate_dates(cls, values):
    """
    Root validator is used to check all fields of the model.
    :param values: object
    :return: values: object
    """
    if "date_start" in values and "date_end" in values and values["date_end"] < values["date_start"]:
        raise ValueError("date_end should be greater than date_start")
    return values

class BookingsSchemaReceived(BaseModel):
    spaceship_id: PositiveInt
    customer_id: PositiveInt
    date_start: datetime
    date_end: datetime

    @root_validator(pre=True)
    def validate(cls, values):
        """
        Root validator is used to check all fields of the model.
        :param values: object
        :return: values: object
        """
        return validate_dates(cls, values)
    class Config:
        from_attributes = True


class BookingsSchemaStored(BaseModel):
    id: PositiveInt
    spaceship_id: PositiveInt
    customer_id: PositiveInt
    date_start: datetime
    date_end: datetime

    # Root validator skipped it is checked on receiving stage
    class Config:
        from_attributes = True
