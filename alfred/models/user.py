from pydantic import BaseModel, validator
from datetime import date
import re


class User(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    birthday: date

    def __str__(self):
        return "user"


@validator("phone_number")
def valid_quantity(cls, value):
    e164_pattern = r"^\+?[1-9]\d{1,14}$"
    phone_number = re.match(e164_pattern, value)
    if not phone_number and not len(value) != len(phone_number):
        raise ValueError("invalid phone number ")
    return value
