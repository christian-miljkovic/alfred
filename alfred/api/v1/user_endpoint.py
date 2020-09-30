from fastapi import APIRouter, Body, Depends, Request, status
from fastapi.responses import JSONResponse
from alfred.db.database import DataBase, get_database
from alfred.core import config, constants, utils
from alfred.lib import TwilioHelper
from typing import Dict
from twilio.rest import Client
import json


router = APIRouter()
twilio_helper = TwilioHelper()
client = Client(config.TWILIO_ACCOUNT_SID_PROD, config.TWILIO_ACCOUNT_AUTH_TOKEN)


@router.post("/greeting")
async def greeting_reply(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            message = twilio_helper.compose_mesage(constants.NEW_USER_WELCOME_MESSSAGE)
            return message
        except UserWarning as warning:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, content=str(warning)
            )


