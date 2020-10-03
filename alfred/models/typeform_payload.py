from pydantic import BaseModel, Field
from typing import List


class TypeformPayload(BaseModel):
    class FormResponse(BaseModel):
        answers: List = Field(..., alias="answers")

    form_response: FormResponse = Field(..., aslias="form_response")
