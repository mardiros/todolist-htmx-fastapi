from fastapi.testclient import TestClient


def test_serve_index(client: TestClient):
    resp = client.get("/")
    assert '<script src="https://unpkg.com/htmx.org@1.9.2"></script>' in resp.text
    assert '<link href="/static/css/main.css" rel="stylesheet">' in resp.text
    assert "My TODO List" in resp.text
