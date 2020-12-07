from alfred.crud import clients
from alfred.db.database import DataBase, get_database
from fastapi import APIRouter, Depends, Request

router = APIRouter()

@router.post("/recommendations")
async def index(request: Request, db: DataBase = Depends(get_database)):    
    logging.warning('got a recommendation')
    async with db.pool.acquire() as conn:
        try:
            twilio_payload = await processors.twilio_request(request)
            existing_client = await clients.find_client_by_phone(conn, twilio_payload.user_identifier)
            if existing_client:
                req = {"client_id": existing_client.id, "message": twilio_payload.get("current_input","")}
                response = await requests.post(f"{config.RECOMMENDATION_APP_URL}/recommendations", data=json.dumps(req))
                logging.warning(response)
                message = twilio_helper.compose_mesage(f"{constants.RECOMMENDATION_MESSAGE}")
                return message
        except Exception as e:
            logging.error(e)
            failed_message = twilio_helper.compose_mesage(constants.FAILURE_MESSAGE)
            return failed_message
