from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.responses import JSONResponse
from alfred.db.database import DataBase, get_database
from alfred.core import config, utils
from alfred.lib import TwilioHelper
from typing import Dict
from twilio.rest import Client
# import alfred.crud as crud
# import alfred.models as model
# import alfred.core.text_responses as text


router = APIRouter()
twilio_helper = TwilioHelper()
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_ACCOUNT_AUTH_TOKEN)


@router.post("/add_friend")
async def add_item_to_cart(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            body = await request.json()
            msg = dict(body)
            message = client.messages.create(
                body="Jarvis test",
                messaging_service_sid=config.TWILIO_ACCOUNT_MESSAGING_SID,
                to=config.TO_PHONE_NUMBER
            )
            return twilio_helper.compose_mesage(msg)
        except UserWarning as warning:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, content=str(warning)
            )


