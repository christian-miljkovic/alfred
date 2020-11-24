from alfred.crud import clients
from alfred.db.database import DataBase, get_database
from alfred.lib import TwilioHelper, to_client as typeform_to_client
from fastapi import APIRouter, Body, Depends, Request
from twilio.rest import Client as TwilioClient
import logging

router = APIRouter()

@router.post("/")
async def index(request: Request, db: DataBase = Depends(get_database)):
    logging.warning('got the message')
    return {'data': 'got it'}