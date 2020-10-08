from alfred.main import app
from pathlib import Path
from starlette.testclient import TestClient
import alfred.models as model
import alfred.core.config as config
import alfred.crud as crud
import alfred.core.utils as util
import datetime
import json
import pytest

API_PREFIX = "alfred/v1/friend"
test_client = TestClient(app)


@pytest.fixture
def client() -> model.Client:
    return model.Client(
        first_name="Christian",
        last_name="Miljkovic",
        phone_number="+12035724630",
        birthday=datetime.datetime.now(),
    )


@pytest.fixture
async def client_in_db(conn, client) -> model.ClientInDB:
    client_in_db = await crud.clients.create_client(conn, client)
    yield client_in_db
    await crud.clients.delete_client(conn, client_in_db.id)


@pytest.fixture
def friend(client_in_db) -> model.Friend:
    return model.Friend(
        client_id=client_in_db.id,
        first_name="Erick",
        last_name="Marcello",
        phone_number="+12035006397",
        birthday=datetime.datetime.now(),
    )


@pytest.fixture
async def friend_in_db(conn, friend) -> model.FriendInDB:
    friend_in_db = await crud.friends.create_friend(conn, friend)
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
async def test_create_success(conn, client_in_db, friend_in_db, friend_payload, mocker):
    resp = test_client.get(
        f"{API_PREFIX}/{client_in_db.id}/create?token={config.WEBHOOK_SECRET_TOKEN}",
        json=friend_payload,
    )
    expected_resp_data = util.model_list_to_data_dict([friend_in_db])
    expected_resp_byte = util.create_aliased_response(expected_resp_data)
    expected_resp = json.loads(expected_resp_byte.body)

    assert resp.json() == expected_resp
    assert resp.status_code == 200
