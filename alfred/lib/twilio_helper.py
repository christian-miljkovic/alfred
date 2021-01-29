from alfred.core import config
from alfred.core import utils
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import logging

TWILIO_CLIENT = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_ACCOUNT_AUTH_TOKEN)


def compose_mesage(message, memory=None, item_to_add=None):
    response = {"actions": []}
    add_text(response, message)
    if item_to_add and memory:
        remember_this_item(response, memory, item_to_add)

    return utils.create_json_response(response)


def add_text(response: dict, message: str):
    response.get("actions").append({"say": message})


def remember_this_item(current_message, current_memory, item):
    new_order = current_memory.get("order", [])
    item_object = {"item": item.get("id"), "quantity": item.get("quantity")}
    new_order.append(item_object)
    return current_message.get("actions").append({"remember": {"order": new_order}})


def send_direct_message(message, to_phone_number=config.TO_PHONE_NUMBER):
    try:
        message = TWILIO_CLIENT.messages.create(body=message, from_=config.FROM_PHONE_NUMBER, to=to_phone_number)
    except TwilioRestException as error:
        logging.error(f"Error sending twilio message: {error}")
        return
    return message.sid
