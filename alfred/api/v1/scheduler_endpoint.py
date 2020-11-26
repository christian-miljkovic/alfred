from alfred.core import utils
from alfred.crud import friends
from alfred.db.database import DataBase, get_database
from alfred.lib import TwilioHelper, group_friends_by_client_id
from fastapi import APIRouter, Body, Depends, Request, status
from twilio.rest import Client as TwilioClient
import logging

router = APIRouter()

@router.post("/")
async def index(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            resp = await request.json()
            birthday_dict = resp.get("data", {})
            logging.warning(f"response received {resp}")
            birthdays_today = await friends.get_friends_by_date(conn, birthday_dict)
            client_map = group_friends_by_client_id(birthdays_today)
            return utils.create_aliased_response({'data': birthdays_today}, status.HTTP_202_ACCEPTED)
        except Exception as e:
            logging.error(e)
            return utils.create_aliased_response(
                {"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )