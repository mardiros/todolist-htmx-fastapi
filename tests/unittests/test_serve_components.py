from typing import Any, Mapping

import pytest
from fastapi.testclient import TestClient

from todolist.domain.model import TodoListItem
from todolist.domain.repositories import AbstractTodoListRepository
from todolist.service.unit_of_work import AbstractUnitOfWork


@pytest.mark.parametrize(
    "params", [{"todolist": [TodoListItem(label="Buy some milk")]}]
)
async def test_serve_todolist(
    params: Mapping[str, Any],
    todolist_repository: AbstractTodoListRepository,
    client: TestClient,
):
    resp = client.get("/components/todo-list")
    id = params["todolist"][0].id
    assert "Buy some milk&nbsp;" in resp.text
    assert f'hx-delete="/components/todo-list/{id}"' in resp.text
    assert 'hx-trigger="click"' in resp.text


async def test_add_todolist_item(uow: AbstractUnitOfWork, client: TestClient):
    resp = client.post(
        "/components/todo-list",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        content="label=Buy+some+milk",
    )
    assert "<button " in resp.text
    assert "HX-Trigger" in resp.headers
    assert resp.headers["HX-Trigger"] == "reload-todo-list"
    async with uow as uow:
        ret = await uow.todolist.list()
        await uow.rollback()
    assert len(ret) == 1
    assert ret[0].label == "Buy some milk"


@pytest.mark.parametrize(
    "params", [{"todolist": [TodoListItem(label="Buy some milk")]}]
)
async def test_remove_todolist_item(
    params: Mapping[str, Any],
    todolist_repository: AbstractTodoListRepository,
    client: TestClient,
):
    id = params["todolist"][0].id
    resp = client.delete(f"/components/todo-list/{id}")
    assert "HX-Trigger" in resp.headers
    assert resp.headers["HX-Trigger"] == "reload-todo-list"
    assert await todolist_repository.list() == []
