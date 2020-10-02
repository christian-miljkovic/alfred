from alfred.models import TwilioPayload
from fastapi import Request
from starlette.responses import JSONResponse, Response
from twilio.twiml.messaging_response import MessagingResponse
import re


def create_text_response(response: MessagingResponse) -> Response:
    headers = {"Content-Type": "text/plain"}
    return Response(content=str(response), headers=headers)


def create_json_response(message: dict) -> JSONResponse:
    return JSONResponse(message)


async def process_twilio_request(twilio_request: Request) -> TwilioPayload:
    twilio_payload = await twilio_request.form()
    twilio_payload_dict = dict(twilio_payload)

    try:
        return TwilioPayload(**twilio_payload_dict)
    except Exception:
        raise Exception("Failed to process twilio request")


def validate_phone_number(phone_number: str) -> bool:
    if len(phone_number) != 12:
        return False
    e164_pattern = r"^\+?[1-9]\d{1,14}$"
    matched_phone_number = re.match(e164_pattern, phone_number)
    if not matched_phone_number:
        return False

    return True
