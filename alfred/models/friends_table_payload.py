from pydantic import BaseModel


class FriendsTablePayload(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    birthday: str

    def __str__(self):
        return f"first_name: {self.first_name} last_name: {self.last_name} phone_number: {self.phone_number}  birthday: {self.birthday}"
