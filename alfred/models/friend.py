from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from alfred.core import utils


class Friend(BaseModel):
    client_id: UUID
    first_name: str
    last_name: str
    phone_number: str
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
