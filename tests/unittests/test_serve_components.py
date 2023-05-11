import pytest
from fastapi.testclient import TestClient

from todolist.domain.model import TodoListItem
from todolist.domain.repositories import AbstractTodoListRepository


@pytest.mark.parametrize(
    "params", [{"todolist": [TodoListItem(label="Buy some milk")]}]
)
def test_serve_todolist(
    todolist_repository: AbstractTodoListRepository, client: TestClient
):
    resp = client.get("/components/todo-list")
    assert "<li>Buy some milk</li>" in resp.text
