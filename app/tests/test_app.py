import pytest
import json
from unittest.mock import patch, MagicMock

# Mock redis before importing app
with patch("redis.Redis") as mock_redis:
    mock_redis.return_value = MagicMock()
    from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    m = MagicMock()
    m.lrange.return_value = ["Buy milk", "Learn DevOps"]
    m.ping.return_value = True
    monkeypatch.setattr("app.r", m)
    return m


def test_home_returns_200(client):
    res = client.get("/")
    assert res.status_code == 200


def test_get_todos(client):
    res = client.get("/todos")
    data = json.loads(res.data)
    assert "todos" in data
    assert isinstance(data["todos"], list)


def test_add_todo(client, mock_redis):
    res = client.post("/todos", json={"task": "Test task"})
    assert res.status_code == 201
    mock_redis.rpush.assert_called_once_with("todos", "Test task")


def test_delete_todo(client, mock_redis):
    res = client.delete("/todos/Buy%20milk")
    assert res.status_code == 200
    mock_redis.lrem.assert_called_once()


def test_health_check(client):
    res = client.get("/health")
    data = json.loads(res.data)
    assert data["status"] == "healthy"


def test_metrics_endpoint(client):
    res = client.get("/metrics")
    assert res.status_code == 200
