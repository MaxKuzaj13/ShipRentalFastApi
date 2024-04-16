from pydantic import BaseModel, Field, PositiveInt


class UserSchemaReceived(BaseModel):
    # TODO ADD validator unique user and unique password
    username: str = Field(min_length=5, max_length=255)
    email: str = Field(min_length=5, max_length=255)
    full_name: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=5, max_length=255)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                    "username": "Kora Jackowska",
                    "email": "kora.jackowska1@gmail.com",
                    "full_name": "Kora Jackowska",
                    "password": "Admin123!",
                }

        }


class UserSchemaStored(BaseModel):
    id: PositiveInt
    username: str = Field(min_length=5, max_length=255)
    email: str = Field(min_length=5, max_length=255)
    full_name: str = Field(min_length=5, max_length=255)
    active_user: bool
    hashed_password: str = Field(min_length=5, max_length=255)


    # Validator skipped it is checked on receiving stage

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "Kora Jackowska",
                "email": "kora.jackowska1@gmail.com",
                "full_name": "Kora Jackowska",
                "active_user": True,
                "hashed_password": "$2b$12$1LltEhJ4DwkR2edqVRNZX.aeRAso9zI/wkaBuQc0UZ.DIuTsdvfDi",
            }

        }
