from fastapi.testclient import TestClient


def test_serve_index(client: TestClient):
    resp = client.get("/")
    assert "<h1>My TODO List</h1>" in resp.text
