from alfred.core import config, constants, processors
from alfred.crud import clients
from alfred.db.database import DataBase, get_database
from alfred.lib import twilio_helper
from fastapi import APIRouter, Depends, Request
import logging
import requests

router = APIRouter()


@router.post("/create")
async def index(request: Request, db: DataBase = Depends(get_database)):
    async with db.pool.acquire() as conn:
        try:
            twilio_payload = await processors.twilio_request(request)
            logging.warning(twilio_payload)
            existing_client = await clients.find_client_by_phone(conn, twilio_payload.user_phone_number)

            if existing_client:
                req = {"client_id": str(existing_client.id), "message": str(twilio_payload.current_input)}
                response = requests.post(f"{config.RECOMMENDATION_APP_URL}/recommendations", data=req)
                logging.warning(response.content)
                message = twilio_helper.compose_mesage(f"{constants.RECOMMENDATION_MESSAGE}")
                return message
        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message
