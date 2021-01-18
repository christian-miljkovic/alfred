from alfred.core import config, constants
from alfred.crud import clients
from alfred.main import app
from datetime import datetime
from starlette.testclient import TestClient
from tests.helper import setup_fixture_object

import alfred.models as model
import alfred.crud as crud
import pytest

API_PREFIX = "alfred/v1/client"
test_client = TestClient(app)


@pytest.fixture
def twilio_auto_ml_payload() -> dict:
    return setup_fixture_object("twilio_auto_ml_payload.json")


@pytest.fixture
def typeform_payload() -> dict:
    return setup_fixture_object("type_form_payload.json")


@pytest.fixture
def client() -> model.Client:
    return model.Client(
        first_name="Christian",
        last_name="Miljkovic",
        phone_number="+12035724630",
        birthday=datetime.strptime("1995-01-24", "%Y-%m-%d"),
    )


@pytest.fixture
async def client_in_db(conn, client) -> model.ClientInDB:
    client_in_db = await crud.clients.create_client(conn, client)
    yield client_in_db
    await crud.clients.delete_client(conn, client_in_db.id)


@pytest.mark.asyncio
async def test_index_no_existing_client(conn, twilio_auto_ml_payload, mocker):
    resp = test_client.post(f"{API_PREFIX}/", data=twilio_auto_ml_payload)
    assert resp
    assert resp.status_code == 200
    assert resp.json() == {"actions": [{"say": f"{constants.NEW_CLIENT_WELCOME_MESSSAGE}"}]}


@pytest.mark.asyncio
async def test_index_existing_client(conn, client_in_db, twilio_auto_ml_payload, mocker):
    resp = test_client.post(f"{API_PREFIX}/", data=twilio_auto_ml_payload)
    assert resp
    assert resp.status_code == 200
    assert resp.json() == {
        "actions": [{"say": f"{constants.RETURNING_CLIENT_WELCOME_MESSSAGE} {client_in_db.first_name}"}]
    }


@pytest.mark.asyncio
async def test_create_client(conn, typeform_payload, mocker):
    send_direct_message_mock = mocker.patch(
        "alfred.lib.twilio_helper.send_direct_message", return_value=config.TWILIO_ACCOUNT_SID_DEV
    )
    resp = test_client.post(f"{API_PREFIX}/create", json=typeform_payload)

    # Phone number comes from the fixture
    client_phone_number = "+12037489763"
    expected_client = await clients.find_client_by_phone(conn, client_phone_number)
    client_json_compatible = client_model_to_json(expected_client)

    assert resp
    assert resp.status_code == 200
    assert send_direct_message_mock.assert_called
    assert resp.json() == client_json_compatible


@pytest.mark.asyncio
async def test_show_friends_table(conn, client_in_db, twilio_auto_ml_payload, mocker):
    resp = test_client.post(f"{API_PREFIX}/friends_table", data=twilio_auto_ml_payload)
    assert resp
    assert resp.status_code == 200
    assert resp.json() == {
        "actions": [
            {
                "say": f"Here's the link {config.REACT_APP_URL}/table/{client_in_db.id} let me know if you need anything else!"
            }
        ]
    }


### PRIVATE FUNCTIONS


def client_model_to_json(client):
    client_dict = client.dict()
    client_dict["id"] = str(client_dict["id"])
    client_dict["birthday"] = client_dict["birthday"].strftime("%Y-%m-%d")
    client_dict["created_at"] = client_dict["created_at"].strftime("%Y-%m-%d")
    client_dict["updated_at"] = client_dict["updated_at"].strftime("%Y-%m-%d")
    return client_dict
