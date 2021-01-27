from alfred.core import config
from alfred.main import app
from alfred.models import Client, ClientInDB, Friend, FriendInDB
from datetime import datetime
from typing import List
from starlette.testclient import TestClient
from tests.helper import setup_fixture_object

import alfred.core.utils as utils
import alfred.crud as crud
import json
import pytest
import uuid
import logging

API_PREFIX = "alfred/v1/friend"
test_client = TestClient(app)


@pytest.fixture
def client() -> Client:
    return Client(
        first_name="Christian",
        last_name="Miljkovic",
        phone_number="+12035724630",
        birthday=datetime.strptime("1995-01-24", "%Y-%m-%d"),
    )


@pytest.fixture
async def client_in_db(conn, client) -> ClientInDB:
    client_in_db = await crud.clients.create_client(conn, client)
    yield client_in_db
    await crud.clients.delete_client(conn, client_in_db.id)


@pytest.fixture
def friend_one(client_in_db) -> FriendInDB:
    return Friend(
        id=uuid.uuid4(),
        client_id=client_in_db.id,
        first_name="Christian",
        last_name="Miljkovic",
        phone_number="+12035724630",
        birthday=datetime.strptime("1995-01-24", "%Y-%m-%d"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def friend_two(client_in_db) -> FriendInDB:
    return FriendInDB(
        id=uuid.uuid4(),
        client_id=client_in_db.id,
        first_name="Erick",
        last_name="Marcello",
        phone_number="+12035006397",
        birthday=datetime.strptime("2000-01-24", "%Y-%m-%d"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def friend_list(friend_one, friend_two) -> List[FriendInDB]:
    return [friend_one, friend_two]


@pytest.fixture
async def friend_in_db(conn, friend_one) -> FriendInDB:
    friend_in_db = await crud.friends.create_friend(conn, friend_one)
    yield friend_in_db
    await crud.friends.delete_friend(conn, friend_in_db.id)


@pytest.fixture
async def friends_in_db(conn, friend_list) -> FriendInDB:
    friend_in_db_list = []
    for friend in friend_list:
        created_friend = await crud.friends.create_friend(conn, friend)
        friend_in_db_list.append(created_friend)
    yield friend_in_db_list

    for friend in friend_in_db_list:
        await crud.friends.delete_friend(conn, friend.id)


@pytest.fixture
def friends_payload():
    created_friend = setup_fixture_object("create_friends_payload.json")
    return created_friend


@pytest.fixture(scope="module")
def twilio_collect_birthday_payload():
    return setup_fixture_object("twl_gather_birthday_payload.json")


@pytest.mark.asyncio
async def test_index_success(conn, client_in_db, friend_in_db):
    resp = test_client.get(f"{API_PREFIX}/{client_in_db.id}?token={config.WEBHOOK_SECRET_TOKEN}")
    expected_resp_data = utils.model_list_to_data_dict([friend_in_db])
    expected_resp_byte = utils.create_aliased_response(expected_resp_data)
    expected_resp = json.loads(expected_resp_byte.body)

    assert resp.json() == expected_resp
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_get_single_friend_success(conn, client_in_db, friend_in_db):
    resp = test_client.get(
        f"{API_PREFIX}/{friend_in_db.id}/client/{client_in_db.id}?token={config.WEBHOOK_SECRET_TOKEN}"
    )
    expected_resp_data = utils.create_aliased_response({"data": friend_in_db.dict()})
    expected_resp = json.loads(expected_resp_data.body)

    assert resp.json() == expected_resp
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_create_success(conn, client_in_db, friends_in_db, friends_payload):
    resp = test_client.post(
        f"{API_PREFIX}/{client_in_db.id}/create?token={config.WEBHOOK_SECRET_TOKEN}",
        json=friends_payload,
    )

    assert resp
    assert resp.status_code == 201

    payload_friends = resp.json().get("data")
    matched_friends = set()
    for friend in payload_friends:
        for expected_friend in friends_in_db:
            expected_friend_dict = expected_friend.dict()
            if is_same_friend(friend, expected_friend_dict):
                matched_friends.add(str(friend))

    assert len(matched_friends) == len(friends_in_db)


@pytest.mark.asyncio
async def test_update_success(conn, client_in_db, friend_in_db):
    update_friend_payload = {
        "data": {
            "birthday": "2005-01-24",
            "first_name": "Christian",
            "last_name": "Miljkovic",
            "phone_number": "+12035724630",
        }
    }
    expected_birthday = update_friend_payload.get("data").get("birthday")
    expected_friend = await crud.friends.get_friend_by_id(conn, friend_in_db.id)
    expected_friend.birthday = expected_birthday
    resp = test_client.put(
        f"{API_PREFIX}/{client_in_db.id}/update/{friend_in_db.id}?token={config.WEBHOOK_SECRET_TOKEN}",
        json=update_friend_payload,
    )

    assert resp
    assert resp.status_code == 200
    return resp.json() == {"data": expected_friend}


@pytest.mark.asyncio
async def test_collect_birthdays(conn, client_in_db, friends_in_db, twilio_collect_birthday_payload, mocker):
    send_direct_message_mock = mocker.patch(
        "alfred.lib.twilio_helper.send_direct_message", return_value=config.TWILIO_ACCOUNT_SID_DEV
    )
    resp = test_client.post(
        f"{API_PREFIX}/birthdays/collect?token={config.WEBHOOK_SECRET_TOKEN}",
        data=twilio_collect_birthday_payload,
    )
    assert send_direct_message_mock.assert_called
    # In the endpoint send_direct_message_mock is called twice per friend
    assert send_direct_message_mock.call_count == len(friends_in_db) * 2
    assert resp.status_code == 200
    assert resp.json() == {"actions": [{"say": "Just sent to everyone! Now sit back and let me handle all of it :)"}]}


def is_same_friend(friend_one: dict, friend_two: dict):
    fields = [
        "client_id",
        "first_name",
        "last_name",
        "phone_number",
        "birthday",
        "created_at",
        "updated_at",
    ]
    for field in fields:
        if (field not in friend_one or field not in friend_two) and (friend_one.get(field) != friend_two.get(field)):
            return False
    return True
