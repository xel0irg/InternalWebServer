import json

import pytest

from app import create_app
from links import LinkDataError, load_links


@pytest.fixture
def client():
    return create_app().test_client()


def test_index_renders_links_from_catalogue(client):
    res = client.get("/")
    assert res.status_code == 200
    body = res.data.decode()
    assert "Internal Resource Hub" in body
    assert "Source control" in body
    assert "Development" in body


def test_api_links_returns_catalogue(client):
    data = client.get("/api/links").get_json()
    assert data["categories"][0]["links"][0]["title"] == "Source control"


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


def test_missing_file_raises(tmp_path):
    with pytest.raises(LinkDataError, match="not found"):
        load_links(tmp_path / "nope.json")


def test_invalid_json_raises(tmp_path):
    path = tmp_path / "links.json"
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(LinkDataError, match="Invalid JSON"):
        load_links(path)


def test_link_without_url_raises(tmp_path):
    path = tmp_path / "links.json"
    path.write_text(
        json.dumps({"categories": [{"name": "X", "links": [{"title": "No URL"}]}]}),
        encoding="utf-8",
    )
    with pytest.raises(LinkDataError, match="'title' and a 'url'"):
        load_links(path)


def test_optional_fields_get_defaults(tmp_path):
    path = tmp_path / "links.json"
    path.write_text(
        json.dumps({"categories": [{"name": "X", "links": [{"title": "T", "url": "u"}]}]}),
        encoding="utf-8",
    )
    link = load_links(path)["categories"][0]["links"][0]
    assert link["description"] == ""
    assert link["tags"] == []
