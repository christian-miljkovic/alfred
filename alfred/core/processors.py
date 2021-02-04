from alfred.models import Friend, FriendsTablePayload, TwilioPayload, UpdateFriendPayload
from datetime import datetime
from fastapi import Request
import humps


async def twilio_request(twilio_request: Request) -> TwilioPayload:
    twilio_payload = await twilio_request.form()
    twilio_payload_dict = dict(twilio_payload)
    normalized_twilio_payload = humps.decamelize(twilio_payload_dict)

    try:
        return TwilioPayload(**normalized_twilio_payload)
    except Exception as error:
        raise Exception(f"Failed to process twilio request with error message: {error}")


def friends_table_request(friend_payload, client_id) -> Friend:
    try:
        normalized_friend = humps.decamelize(friend_payload)
        payload = FriendsTablePayload(**normalized_friend)
        return Friend(
            client_id=client_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone_number=payload.phone_number,
        )
    except Exception as error:
        raise Exception(f"Failed to process friends table request with error message: {error}")


def update_friends_table_request(friend_payload, friend_id) -> UpdateFriendPayload:
    try:
        normalized_friend = humps.decamelize(friend_payload)
        return UpdateFriendPayload(id=friend_id, **normalized_friend)
    except Exception as error:
        raise Exception(f"Failed to process update friends table request with error message: {error}")
