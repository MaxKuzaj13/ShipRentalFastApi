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
        Validator for Polish ID numbers

        Args:
            id_number (str): The ID number to be validated.

        Returns:
            str: The validated ID number.
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
        json_schema_extra = {
            "example": {
                    "name": "Kora Jackowska",
                    "address": "Plac Zbawiciela 2, Kraków",
                    "document_number": "ABS123456"
                }

        }


class CustomerSchemaStored(BaseModel):
    id: Optional[PositiveInt]
    name: str = Field(min_length=5, max_length=255)
    address: str = Field(min_length=5, max_length=255)
    document_number: str = Field(min_length=9, max_length=9)

    # Validator skipped it is checked on receiving stage

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                    "id": 5,
                    "name": "Kora Jackowska",
                    "address": "Plac Zbawiciela 2, Kraków",
                    "document_number": "ABS123456"
            }

        }
