from alfred.main import app
from starlette.testclient import TestClient
import alfred.models as model
import alfred.core.config as config
import alfred.crud as crud
import datetime
import logging
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


@pytest.mark.asyncio
async def test_index_success(conn, client_in_db, friend_in_db, mocker):
    resp = test_client.get(
        f"{API_PREFIX}/{client_in_db.id}?token={config.WEBHOOK_SECRET_TOKEN}"
    )
    logging.warning(resp)
    logging.warning(
        f"{API_PREFIX}/{client_in_db.id}?token={config.WEBHOOK_SECRET_TOKEN}"
    )
    assert resp.status_code == 200
