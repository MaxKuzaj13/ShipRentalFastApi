from pydantic import BaseModel, Field, PositiveInt, validator
from validate_email_address import validate_email


class UserSchemaReceived(BaseModel):
    username: str = Field(min_length=4, max_length=255)
    email: str = Field(min_length=5, max_length=255)
    full_name: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=5, max_length=255)

    @validator("email")
    def validate_email(cls, email):
        if not validate_email(email):
            raise ValueError("Invalid email format")
        return email
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "Kora",
                "email": "kora.jackowska1@gmail.com",
                "full_name": "Kora Jackowska",
                "password": "Admin123!",
            }

        }


class UserSchemaStored(BaseModel):
    id: PositiveInt
    username: str = Field(min_length=4, max_length=255)
    email: str = Field(min_length=5, max_length=255)
    full_name: str = Field(min_length=5, max_length=255)
    active_user: bool
    hashed_password: str = Field(min_length=5, max_length=255)

    # Validator skipped it is checked on receiving stage

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "Kora",
                "email": "kora.jackowska1@gmail.com",
                "full_name": "Kora Jackowska",
                "active_user": True,
                "hashed_password": "$2b$12$1LltEhJ4DwkR2edqVRNZX.aeRAso9zI/wkaBuQc0UZ.DIuTsdvfDi",
            }

        }
