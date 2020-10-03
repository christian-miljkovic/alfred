from starlette.responses import JSONResponse, Response
from twilio.twiml.messaging_response import MessagingResponse
import re


def create_text_response(response: MessagingResponse) -> Response:
    headers = {"Content-Type": "text/plain"}
    return Response(content=str(response), headers=headers)


def create_json_response(message: dict) -> JSONResponse:
    return JSONResponse(message)


def validate_phone_number(phone_number: str) -> bool:
    if len(phone_number) != 12:
        return False
    e164_pattern = r"^\+?[1-9]\d{1,14}$"
    matched_phone_number = re.match(e164_pattern, phone_number)
    if not matched_phone_number:
        return False

    return True
