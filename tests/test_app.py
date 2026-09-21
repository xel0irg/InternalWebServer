import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_index_serves_html(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"InternalWebServer" in res.data


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_api_info(client):
    data = client.get("/api/info").get_json()
    assert data["app"] == "InternalWebServer"
    assert data["uptime_seconds"] >= 0


def test_unknown_route_returns_json_404(client):
    res = client.get("/does-not-exist")
    assert res.status_code == 404
    assert res.get_json() == {"error": "not found"}
