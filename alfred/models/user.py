from pydantic import BaseModel, validator
from datetime import date
from alfred.core.utils import validate_phone_number


class User(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    birthday: date

    def __str__(self):
        return "user"


@validator("phone_number")
def valid_quantity(cls, value):
    if not validate_phone_number:
        raise ValueError("invalid phone number ")
    return value
