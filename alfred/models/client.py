from pydantic import BaseModel, validator
from datetime import date
from alfred.core import utils


class Client(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    birthday: date

    def __str__(self):
        return "client"


class ClientInDB(Client):
    created_at: date
    updated_at: date


@validator("phone_number")
def valid_quantity(cls, value):
    if not utils.validate_phone_number:
        raise ValueError("invalid phone number ")
    return value
