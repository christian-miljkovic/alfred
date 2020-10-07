from alfred import __version__
from alfred.main import app
from starlette.testclient import TestClient

client = TestClient(app)


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
