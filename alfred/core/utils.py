from alfred.core import constants
from fastapi.encoders import jsonable_encoder
from fastapi import status
from starlette.responses import JSONResponse, Response
from twilio.twiml.messaging_response import MessagingResponse
from typing import DefaultDict, List
import re


def create_text_response(response: MessagingResponse) -> Response:
    headers = {"Content-Type": "text/plain"}
    return Response(content=str(response), headers=headers)


def model_list_to_data_dict(model_list: list) -> dict:
    return {"data": [model.dict() for model in model_list]}


def create_json_response(payload: dict) -> JSONResponse:
    return JSONResponse(payload)


def create_aliased_response(payload, status_code=status.HTTP_200_OK) -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder(payload, by_alias=True), status_code=status_code
    )

def create_birthday_reminder_responses(payload: DefaultDict) -> List[str]:
    # convert to messages 
    pass

def validate_phone_number(phone_number: str) -> bool:
    if len(phone_number) != 12:
        return False
    e164_pattern = r"^\+?[1-9]\d{1,14}$"
    matched_phone_number = re.match(e164_pattern, phone_number)
    if not matched_phone_number:
        return False

    return True
