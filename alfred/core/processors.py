from alfred.models import TwilioPayload
from fastapi import Request
import humps
import logging


async def twilio_request(twilio_request: Request) -> TwilioPayload:
    twilio_payload = await twilio_request.form()
    twilio_payload_dict = dict(twilio_payload)
    normalized_twilio_payload = humps.decamelize(twilio_payload_dict)
    logging.warning(normalized_twilio_payload)

    try:
        return TwilioPayload(**normalized_twilio_payload)
    except Exception as error:
        raise Exception(f"Failed to process twilio request with error message: {error}")