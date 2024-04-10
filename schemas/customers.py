from pydantic import BaseModel, validator, PositiveInt, Field
from typing import Optional
from string import ascii_uppercase


class CustomerSchemaReceived(BaseModel):
    name: str = Field(min_length=5, max_length=255)
    address: str = Field(min_length=5, max_length=255)
    document_number: str = Field(min_length=9, max_length=9)

    @validator('document_number')
    def validate_id_number(cls, id_number: str) -> str:
        """
        Validator for polish id numbers
        :param id_numbber: str
        :return: str
        """
        check_numbers = [7, 3, 1, 7, 3, 1, 7, 3]
        values = [int(char) if char.isnumeric() else ascii_uppercase.find(char) + 10 for char in id_number]
        control_number = values.pop(3)
        sum_control = sum(check_numbers * values for check_numbers, values in zip(check_numbers, values))
        if sum_control % 10 != control_number:
            raise ValueError("Document number is not valid")
        return id_number

    class Config:
        from_attributes = True


class CustomerSchemaStored(BaseModel):
    id: Optional[PositiveInt]
    name: str = Field(min_length=5, max_length=255)
    address: str = Field(min_length=5, max_length=255)
    document_number: str = Field(min_length=9, max_length=9)

    # Validator skipped it is checked on receiving stage

    class Config:
        from_attributes = True