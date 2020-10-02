from alfred.db.database import DataBase, get_database
from alfred.core import config, constants
from alfred.crud import clients
from alfred.models import Client
from alfred.lib import TwilioHelper
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from twilio.rest import Client as TwilioClient
import datetime

import logging

router = APIRouter()
twilio_helper = TwilioHelper()
client = TwilioClient(config.TWILIO_ACCOUNT_SID_PROD, config.TWILIO_ACCOUNT_AUTH_TOKEN)


@router.post("/greeting")
async def greeting_reply(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            body = await request.form()
            logging.warning(body)
            # incoming_phone_number = request
            user_dict = {
                "first_name": "Christian",
                "last_name": "Miljkovic",
                "phone_number": "+12035724630",
                "birthday": datetime.datetime.now(),
            }
            new_user = Client(**user_dict)
            created_user = await clients.create_user(conn, new_user)
            if created_user:
                return twilio_helper.compose_mesage(
                    f"constants.RETURNING_USER_WELCOME_MESSSAGE {created_user.first_name}"
                )
            message = twilio_helper.compose_mesage(constants.NEW_USER_WELCOME_MESSSAGE)
            return message
        except UserWarning as warning:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED, content=str(warning)
            )
