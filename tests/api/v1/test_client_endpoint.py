from alfred.main import app
from datetime import datetime
from starlette.testclient import TestClient
import alfred.models as model
import alfred.core.config as config
import alfred.crud as crud
import pytest

API_PREFIX = "alfred/v1/client"
test_client = TestClient(app)


@pytest.fixture
def twilio_auto_ml_payload() -> dict:
    return {
        "current_task": "show_friends_table",
        "current_input": "show friends table",
        "dialogue_sid": "UK2c1d353d522f412aaa8b683123336fb7",
        "memory": '{"twilio":{"chat":{"ChannelSid":"CH5b55ab5dbb90479a819c4ae4837f91e3","AssistantName":"","Attributes":{},"ServiceSid":"IS1000c83233e94e54a734966826f3860e","Index":18,"From":"user","MessageSid":"IM8d89997317204139808711f1db18208f"}}}',
        "dialogue_payloadUrl": "https://autopilot.twilio.com/v1/Assistants/UA58606944b477809f3293100b84e101f4/Dialogues/UK2c1d353d522f412aaa8b683123336fb7",
        "channel": "chat",
        "next_best_task": "",
        "current_task_confidence": "1.0",
        "assistant_sid": "UA58606944b477809f3293100b84e101f4",
        "user_identifier": "+12035724630",
        "account_sid": "ACa03daa661a1b21557ecef006fd7ec3b1",
    }


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
