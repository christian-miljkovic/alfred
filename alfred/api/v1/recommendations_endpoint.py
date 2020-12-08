from alfred.core import config, constants, processors, utils
from alfred.crud import clients
from alfred.db.database import DataBase, get_database
from alfred.lib import TwilioHelper
from fastapi import APIRouter, Depends, Request
import logging
import json
import requests

twilio_helper = TwilioHelper()

router = APIRouter()

@router.post("/create")
async def index(request: Request, db: DataBase = Depends(get_database)):    
    logging.warning('got a recommendation')
    async with db.pool.acquire() as conn:
        try:
            twilio_payload = await processors.twilio_request(request)
            logging.warning(twilio_payload)
            existing_client = await clients.find_client_by_phone(conn, twilio_payload.user_identifier)
            if existing_client:
                req = {"client_id": str(existing_client.id), "message": twilio_payload.current_input}
                response = requests.post(f"{config.RECOMMENDATION_APP_URL}/recommendations", data=json.dumps(req))
                logging.warning(response)
                message = twilio_helper.compose_mesage(f"{constants.RECOMMENDATION_MESSAGE}")
                return message
        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message
