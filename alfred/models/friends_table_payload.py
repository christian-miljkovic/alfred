from pydantic import BaseModel


class FriendsTablePayload(BaseModel):
    first_name: str = None
    last_name: str = None
    phone_number: str = None

    def __str__(self):
        return f"first_name: {self.first_name} last_name: {self.last_name} phone_number: {self.phone_number}"
