import pytest
from fastapi.testclient import TestClient

from todolist.domain.model import TodoListItem
from todolist.domain.repositories import AbstractTodoListRepository
from todolist.service.unit_of_work import AbstractUnitOfWork


@pytest.mark.parametrize(
    "params", [{"todolist": [TodoListItem(label="Buy some milk")]}]
)
def test_serve_todolist(
    todolist_repository: AbstractTodoListRepository, client: TestClient
):
    resp = client.get("/components/todo-list")
    assert "<li>Buy some milk</li>" in resp.text


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
