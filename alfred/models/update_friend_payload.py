from datetime import date
from pydantic import BaseModel
from uuid import UUID


class UpdateFriendPayload(BaseModel):
    id: UUID
    birthday: date

    def __str__(self):
        return f"id: {self.id} birthday: {self.birthday}"
