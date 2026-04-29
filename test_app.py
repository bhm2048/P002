import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# --- /api/echo ---

def test_echo_returns_original_fields(client):
    res = client.post("/api/echo", json={"msg": "hello", "value": 42})
    assert res.status_code == 200
    data = res.get_json()
    assert data["msg"] == "hello"
    assert data["value"] == 42


def test_echo_adds_received_at(client):
    res = client.post("/api/echo", json={"x": 1})
    data = res.get_json()
    assert "received_at" in data


def test_echo_received_at_is_valid_iso(client):
    from datetime import datetime
    res = client.post("/api/echo", json={"x": 1})
    received_at = res.get_json()["received_at"]
    # 確保可以正常解析為 datetime
    dt = datetime.fromisoformat(received_at)
    assert dt is not None


def test_echo_non_json_returns_415(client):
    res = client.post("/api/echo", data="not json", content_type="text/plain")
    assert res.status_code == 415
    assert "error" in res.get_json()


def test_echo_get_not_allowed(client):
    res = client.get("/api/echo")
    assert res.status_code == 405


def test_echo_empty_object(client):
    res = client.post("/api/echo", json={})
    assert res.status_code == 200
    data = res.get_json()
    assert "received_at" in data
    assert len(data) == 1


def test_echo_nested_payload(client):
    payload = {"user": {"name": "Alice"}, "tags": [1, 2, 3]}
    res = client.post("/api/echo", json=payload)
    data = res.get_json()
    assert data["user"]["name"] == "Alice"
    assert data["tags"] == [1, 2, 3]
