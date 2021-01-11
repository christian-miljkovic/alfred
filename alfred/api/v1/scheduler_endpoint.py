from alfred.core import constants, utils
from alfred.crud import clients, friends
from alfred.db.database import DataBase, get_database
from alfred.lib import TwilioHelper, group_friends_by_client_id
from fastapi import APIRouter, Body, Depends, Request, status
from twilio.rest import Client as TwilioClient
import logging

router = APIRouter()
twilio_helper = TwilioHelper()


@router.post("/")
async def index(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            resp = await request.json()
            birthday_data = resp.get("data", {})
            logging.warning(f"response received {resp}")
            birthdays_today = await friends.get_friends_by_date(conn, birthday_data)
            client_map = group_friends_by_client_id(birthdays_today)
            phone_number_to_msg_map = dict()
            for client_id, friend_names in client_map.items():
                client = await clients.find_client_by_id(conn, client_id)
                if client:
                    phone_number_to_msg_map[client.phone_number] = constants.BIRTHDAY_REMINDER_MESSAGE(friend_names)

            for phone_number, message in phone_number_to_msg_map.items():
                twilio_helper.send_direct_message(message, phone_number)

            return utils.create_aliased_response({"data": phone_number_to_msg_map}, status.HTTP_202_ACCEPTED)
        except Exception as e:
            logging.error(e)
            return utils.create_aliased_response(
                {"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )