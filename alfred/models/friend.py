from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import date
from alfred.core import utils


class Friend(BaseModel):
    client_id: str = Field(None, alias="id")
    first_name: str = Field(None, alias="firstName")
    last_name: str = Field(None, alias="lastName")
    phone_number: str = Field(None, alias="phoneNumber")
    birthday: date

    def __str__(self):
        return "friend"


class FriendInDB(Friend):
    id: UUID
    created_at: date
    updated_at: date


@validator("phone_number")
def valid_quantity(cls, value):
    if not utils.validate_phone_number:
        raise ValueError("invalid phone number ")
    return value
