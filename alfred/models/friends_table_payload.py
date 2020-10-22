from pydantic import BaseModel, Field
from uuid import UUID


class FriendsTablePayload(BaseModel):
    client_id: UUID = Field(None, alias="id")
    first_name: str = Field(None, alias="firstName")
    last_name: str = Field(None, alias="lastName")
    phone_number: str = Field(None, alias="phoneNumber")
    birthday: str = Field(None, alias="birthday")

    def __str__(self):
        return "friend"
