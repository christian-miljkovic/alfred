from alfred.db.database import DataBase, get_database
from alfred.core import config, constants, utils
from alfred.crud import clients
from alfred.lib import TwilioHelper
from fastapi import APIRouter, Depends, Request
from twilio.rest import Client as TwilioClient
import logging

router = APIRouter()
twilio_helper = TwilioHelper()
client = TwilioClient(config.TWILIO_ACCOUNT_SID_PROD, config.TWILIO_ACCOUNT_AUTH_TOKEN)


@router.post("/")
async def index(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            twilio_payload = await utils.process_twilio_request(request)
            existing_client = await clients.find_client_by_phone(
                conn, twilio_payload.user_identifier
            )
            if existing_client:
                return twilio_helper.compose_mesage(
                    f"{constants.RETURNING_CLIENT_WELCOME_MESSSAGE} {existing_client.first_name}"
                )
            message = twilio_helper.compose_mesage(
                f"{constants.NEW_CLIENT_WELCOME_MESSSAGE}"
            )
            return message
        except Exception as e:
            logging.error(e)
            failed_message = message = twilio_helper.compose_mesage(
                constants.FAILURE_MESSAGE
            )
            return failed_message


@router.post("/create")
async def create(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            logging.warning(request)

        except Exception as e:
            logging.error(e)
