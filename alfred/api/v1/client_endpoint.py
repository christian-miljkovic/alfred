from alfred.db.database import DataBase, get_database
from alfred.core import config, constants, processors
from alfred.crud import clients
from alfred.lib import TwilioHelper, to_client as typeform_to_client
from fastapi import APIRouter, Body, Depends, Request
from twilio.rest import Client as TwilioClient
from typing import Dict
import alfred.models as models
import logging

router = APIRouter()
twilio_helper = TwilioHelper()
client = TwilioClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_ACCOUNT_AUTH_TOKEN)


@router.post("/")
async def index(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            twilio_payload = await processors.twilio_request(request)
            existing_client = await clients.find_client_by_phone(conn, twilio_payload.user_phone_number)
            if existing_client:
                return twilio_helper.compose_mesage(
                    f"{constants.RETURNING_CLIENT_WELCOME_MESSSAGE} {existing_client.first_name}"
                )
            message = twilio_helper.compose_mesage(f"{constants.NEW_CLIENT_WELCOME_MESSSAGE}")
            return message
        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message


@router.post("/create")
async def create(payload: Dict = Body(...), db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            typeform_payload = models.TypeformPayload(**payload)
            new_client = typeform_to_client(typeform_payload)
            client_in_db = await clients.create_client(conn, new_client)

            if client_in_db:
                message_to_send = constants.REDIRECT_TO_FRIENDS_TABLE(client_in_db.id)
                to_phone_number = client_in_db.phone_number
                twilio_helper.send_direct_message(message_to_send, to_phone_number)
                return client_in_db

            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)

        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message


@router.post("/friends_table")
async def show_friends_table(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            twilio_payload = await processors.twilio_request(request)
            client = await clients.find_client_by_phone(conn, twilio_payload.user_phone_number)
            message_to_send = constants.GET_FRIENDS_TABLE(str(client.id))
            logging.warning(message_to_send)
            return twilio_helper.compose_mesage(f"{message_to_send}")
        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message
