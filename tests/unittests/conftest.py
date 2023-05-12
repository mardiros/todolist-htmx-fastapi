from typing import AsyncIterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from todolist.adapters.repositories import InMemoryUnitOfWork
from todolist.config import Settings
from todolist.domain.repositories import AbstractTodoListRepository
from todolist.entrypoint import bootstrap
from todolist.service.unit_of_work import AbstractUnitOfWork


class ConfiguredOnce:
    app: FastAPI | None = None


@pytest.fixture()
def app_settings() -> Settings:
    return Settings()


@pytest.fixture()
async def uow(app_settings: Settings) -> AsyncIterator[AbstractUnitOfWork]:
    uow = InMemoryUnitOfWork(app_settings)
    yield uow
    uow.todolist.items.clear()  # type: ignore


@pytest.fixture()
async def app(app_settings: Settings, uow: AbstractUnitOfWork) -> FastAPI:
    if ConfiguredOnce.app:
        app = ConfiguredOnce.app
    else:
        app_settings.uow = uow
        app = await bootstrap(app_settings)
        ConfiguredOnce.app = app
    return app


@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)


@pytest.fixture
async def todolist_repository(
    params, uow: AbstractUnitOfWork
) -> AbstractTodoListRepository:
    async with uow as uow:
        for item in params["todolist"]:
            await uow.todolist.add(item)
        return uow.todolist
