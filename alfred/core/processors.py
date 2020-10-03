from alfred.models import TwilioPayload
from fastapi import Request


async def twilio_request(twilio_request: Request) -> TwilioPayload:
    twilio_payload = await twilio_request.form()
    twilio_payload_dict = dict(twilio_payload)

    try:
        return TwilioPayload(**twilio_payload_dict)
    except Exception:
        raise Exception("Failed to process twilio request")