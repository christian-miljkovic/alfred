from alfred.db.database import DataBase, get_database
from alfred.core import config, constants, utils
from alfred.crud import friends
from alfred.lib import TwilioHelper
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from twilio.rest import Client as TwilioClient
from typing import Dict
import alfred.models as models
import logging

router = APIRouter()
twilio_helper = TwilioHelper()
client = TwilioClient(config.TWILIO_ACCOUNT_SID_PROD, config.TWILIO_ACCOUNT_AUTH_TOKEN)


@router.get("/{client_id}")
async def index(client_id: str, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            client_friends = await friends.get_all_friends_by_client_id(conn, client_id)
            resp_data = utils.model_list_to_data_dict(client_friends)
            resp = utils.create_aliased_response(resp_data)
            return resp

        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message


@router.post("/{client_id}/create")
async def create_friends(
    client_id: str, payload: Dict = Body(...), db: DataBase = Depends(get_database)
):
    async with db.pool.acquire() as conn:
        try:
            new_friends = payload.get("friends")
            for friend in new_friends:
                new_friend = models.Friend(client_id=client_id, **new_friends)
                friends.create_friend(conn, new_friend)

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=str("Successfully added friends"),
            )

        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message
