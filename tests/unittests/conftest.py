import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from todolist.config import Settings
from todolist.entrypoint import bootstrap


class ConfiguredOnce:
    app: FastAPI | None = None


@pytest.fixture()
async def app() -> FastAPI:
    settings = Settings()
    if ConfiguredOnce.app:
        app = ConfiguredOnce.app
    else:
        app = await bootstrap(settings)
        ConfiguredOnce.app = app
    return app


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)
