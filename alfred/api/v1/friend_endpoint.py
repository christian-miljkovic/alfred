from alfred.db.database import DataBase, get_database
from alfred.core import config, constants, utils
from alfred.crud import friends
from alfred.lib import TwilioHelper
from fastapi import APIRouter, Body, Depends, status
from twilio.rest import Client as TwilioClient
from typing import Dict
import alfred.models as models
from datetime import datetime
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
            created_friends = []
            friends_list = payload.get("data")
            for friend in friends_list:
                new_friend = models.Friend(
                    client_id=client_id,
                    first_name=friend.get("first_name"),
                    last_name=friend.get("last_name"),
                    phone_number=friend.get("phone_number"),
                    birthday=datetime.strptime(friend.get("birthday"), "%m-%d-%Y"),
                )
                friend_in_db = await friends.create_friend(conn, new_friend)
                created_friends.append(friend_in_db)
                resp = utils.model_list_to_data_dict(created_friends)
            return utils.create_aliased_response(resp, status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message
