from fastapi.testclient import TestClient


def test_serve_todolist(client: TestClient):
    resp = client.get("/components/todo-list")
    assert "<li>Buy some milk</li>" in resp.text
