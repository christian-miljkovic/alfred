from alfred import __version__
from alfred.main import app
from alfred.models import app
from starlette.testclient import TestClient

client = TestClient(app)

@pytest.fixture(scope="session")
def friend() -> model.Friend:
    return model.Friend(
        client_id=uuid4(),
        first_name="Christian",
        last_name="Miljkovic",
        phone_number="+12035724630",
        birthday=datetime.datetime.now(),
    )


def test_version():
    assert __version__ == "0.1.0"


def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == ":)"


def test_api_v1_health_check():
    resp = client.get("/alfred/v1/health")
    assert resp.status_code == 200
    assert resp.json() == ":)"
