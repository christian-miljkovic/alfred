from alfred.db.database import DataBase, get_database
from alfred.core import config, constants, processors, utils
from alfred.crud import clients, friends
from alfred.lib import twilio_helper
from datetime import datetime
from fastapi import APIRouter, Body, Depends, Request, status
from twilio.rest import Client as TwilioClient
from typing import Dict
import alfred.models as models
import logging

router = APIRouter()
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


@router.get("/{friend_id}/client/{client_id}")
async def get_single_friend(friend_id: str, client_id: str, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            friend_in_db = await friends.get_friend_by_id_and_client_id(conn, friend_id, client_id)
            resp = utils.create_aliased_response({"data": friend_in_db.dict()})
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
                new_friend = processors.friends_table_request(friend, client_id)
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


@router.put("/{client_id}/update/{friend_id}")
async def update_friend(
    client_id: str, friend_id: str, payload: Dict = Body(...), db: DataBase = Depends(get_database)
):
    async with db.pool.acquire() as conn:
        try:
            friend = payload.get("data")
            friend_to_update = processors.update_friends_table_request(friend, friend_id)
            update_friend = await friends.update_friend_by_id(conn, friend_to_update)
            return utils.create_aliased_response({"data": update_friend}, status.HTTP_200_OK)

        except Exception as e:
            logging.error(e)
            return utils.create_aliased_response(
                {"error": constants.FAILURE_MESSAGE},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


@router.delete("/{friend_id}")
async def delete_friends(friend_id: str, payload: Dict = Body(...), db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            logging.warning("test test")
            friend = payload.get("data")
            payload = models.FriendsTablePayload(**friend)
            deleted_friend = await friends.delete_friend(conn, friend_id)
            resp = {"data": str(deleted_friend.dict())}
            return utils.create_aliased_response(resp, status.HTTP_202_ACCEPTED)

        except Exception as e:
            logging.error(e)
            return utils.create_aliased_response(
                {"error": constants.FAILURE_MESSAGE},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


@router.post("/birthdays/collect")
async def collect_birthdays(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            twilio_payload = await processors.twilio_request(request)
            client = await clients.find_client_by_phone(conn, twilio_payload.user_phone_number)
            logging.warning(client.dict())
            client_friends = await friends.get_all_friends_by_client_id(conn, client.id)
            logging.warning(client_friends)
            for friend in client_friends:
                # could use a test to prove that the correct message is sent
                message_to_send = constants.SHOW_BIRTHDAY_FORM_MESSAGE(
                    client.id, friend.id, client.first_name, client.last_name, friend.first_name
                )
                logging.warning(message_to_send)

                if not friend.birthday:
                    twilio_helper.send_direct_message(message_to_send, friend.phone_number)

            return twilio_helper.compose_mesage(constants.SUCCESS_BIRTHDAY_GATHER_MESSAGE)
        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message
