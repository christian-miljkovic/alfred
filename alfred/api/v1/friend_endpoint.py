from alfred.db.database import DataBase, get_database
from alfred.core import config, constants, utils
from alfred.crud import friends
from alfred.lib import TwilioHelper
from datetime import datetime
from fastapi import APIRouter, Body, Depends, status
from twilio.rest import Client as TwilioClient
from typing import Dict
import alfred.models as models
import logging

router = APIRouter()
twilio_helper = TwilioHelper()
client = TwilioClient(config.TWILIO_ACCOUNT_SID, config.TWILIO_ACCOUNT_AUTH_TOKEN)


@router.get("/{client_id}")
async def index(client_id: str, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            client_friends = await friends.get_all_friends_by_client_id(conn, client_id)
            friend_payload = client_friends if client_friends else []
            resp_data = utils.model_list_to_data_dict(friend_payload)
            resp = utils.create_aliased_response(resp_data)
            return resp

        except Exception as e:
            logging.error(e)
            return utils.create_aliased_response(
                {"error": constants.FAILURE_MESSAGE},
                status_code=status.HTTP_404_NOT_FOUND,
            )


@router.post("/{client_id}/create")
async def create_friends(client_id: str, payload: Dict = Body(...), db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            created_friends = []
            friends_list = payload.get("data")
            for friend in friends_list:
                payload = models.FriendsTablePayload(**friend)
                new_friend = models.Friend(
                    client_id=client_id,
                    first_name=payload.first_name,
                    last_name=payload.last_name,
                    phone_number=payload.phone_number,
                    birthday=datetime.strptime(payload.birthday, "%Y-%m-%d"),
                )
                friend_in_db = await friends.create_friend(conn, new_friend)
                created_friends.append(friend_in_db)

            resp = utils.model_list_to_data_dict(created_friends)
            return utils.create_aliased_response(resp, status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return utils.create_aliased_response(
                {"error": constants.FAILURE_MESSAGE},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


@router.post("/{client_id}/delete")
async def create_friends(client_id: str, payload: Dict = Body(...), db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            friend = payload.get("data")
            payload = models.FriendsTablePayload(**friend)
            new_friend = models.Friend(
                client_id=client_id,
                first_name=payload.first_name,
                last_name=payload.last_name,
                phone_number=payload.phone_number,
                birthday=datetime.strptime(payload.birthday, "%Y-%m-%d"),
            )

            # TO SEND BACK DELETION MESSAGE
            deleted_friend = await friends.delete_friend(conn, new_friend)
            message = "client with id: {client_id} successfully deleted {}"
            resp = {"data": "client with id: {client_id} successfully delete "}

            return utils.create_aliased_response(resp, status.HTTP_202_ACCEPTED)

        except Exception as e:
            logging.error(e)
            return utils.create_aliased_response(
                {"error": constants.FAILURE_MESSAGE},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
