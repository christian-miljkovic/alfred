from alfred.main import app
from datetime import datetime
from pathlib import Path
from typing import List
from starlette.testclient import TestClient
import alfred.models as model
import alfred.core.config as config
import alfred.crud as crud
import alfred.core.utils as util
import json
import pytest
import uuid

API_PREFIX = "alfred/v1/friend"
test_client = TestClient(app)


@pytest.fixture
def client() -> model.Client:
    return model.Client(
        first_name="Christian",
        last_name="Miljkovic",
        phone_number="+12035724630",
        birthday=datetime.strptime("01-24-1995", "%m-%d-%Y"),
    )


@pytest.fixture
async def client_in_db(conn, client) -> model.ClientInDB:
    client_in_db = await crud.clients.create_client(conn, client)
    yield client_in_db
    await crud.clients.delete_client(conn, client_in_db.id)


@pytest.fixture
def friend_one(client_in_db) -> model.FriendInDB:
    return model.Friend(
        id=uuid.uuid4(),
        client_id=client_in_db.id,
        first_name="Christian",
        last_name="Miljkovic",
        phone_number="+12035724630",
        birthday=datetime.strptime("01-24-1995", "%m-%d-%Y"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def friend_two(client_in_db) -> model.FriendInDB:
    return model.FriendInDB(
        id=uuid.uuid4(),
        client_id=client_in_db.id,
        first_name="Erick",
        last_name="Marcello",
        phone_number="+12035006397",
        birthday=datetime.strptime("01-24-2000", "%m-%d-%Y"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def friend_list(friend_one, friend_two) -> List[model.FriendInDB]:
    return [friend_one, friend_two]


@pytest.fixture
async def friend_in_db(conn, friend_one) -> model.FriendInDB:
    friend_in_db = await crud.friends.create_friend(conn, friend_one)
    yield friend_in_db
    await crud.friends.delete_friend(conn, friend_in_db.id)


@pytest.fixture(scope="module")
def friend_payload():
    fixture_data_folder = Path().cwd() / Path("tests/fixtures")
    fixture_data_file = fixture_data_folder / "create_client_payload.json"
    with open(fixture_data_file) as json_file:
        return json.load(json_file)


@pytest.mark.asyncio
async def test_index_success(conn, client_in_db, friend_in_db, mocker):
    resp = test_client.get(
        f"{API_PREFIX}/{client_in_db.id}?token={config.WEBHOOK_SECRET_TOKEN}"
    )
    expected_resp_data = util.model_list_to_data_dict([friend_in_db])
    expected_resp_byte = util.create_aliased_response(expected_resp_data)
    expected_resp = json.loads(expected_resp_byte.body)

    assert resp.json() == expected_resp
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_create_success(conn, client_in_db, friend_list, friend_payload, mocker):
    resp = test_client.post(
        f"{API_PREFIX}/{client_in_db.id}/create?token={config.WEBHOOK_SECRET_TOKEN}",
        json=friend_payload,
    )
    expected_resp_data = util.model_list_to_data_dict(friend_list)
    resp_dict = dict(resp.json())
    result = resp_dict.get("data")
    expected_result = expected_resp_data.get("data")
    assert result
    assert resp.status_code == 201

    matched_friends = []
    for friend in result:
        for expected_friend in expected_result:
            if is_same_friend(friend, expected_friend):
                matched_friends.append(
                    {friend.get("client_id"), str(expected_friend.get("client_id"))}
                )

    assert len(matched_friends) == len(expected_result)


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
        if (field not in friend_one or field not in friend_two) and (
            friend_one.get(field) != friend_two.get(field)
        ):
            return False
    return True
