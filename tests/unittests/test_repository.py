from typing import Any, Mapping

import pytest

from todolist.domain.model import TodoListItem
from todolist.domain.repositories import AbstractTodoListRepository


@pytest.mark.parametrize("params", [{"todolist": []}])
async def test_inmemorytodolist_repository(
    todolist_repository: AbstractTodoListRepository,
):
    repo = todolist_repository
    await repo.add(TodoListItem(label="Build the package"))
    todo = await repo.list()
    assert todo == [TodoListItem(id=todo[0].id, label="Build the package")]


@pytest.mark.parametrize(
    "params",
    [
        {
            "todolist": [
                TodoListItem(label="Create repository"),
                TodoListItem(label="Write code"),
                TodoListItem(label="Build the package"),
            ]
        }
    ],
)
async def test_inmemorytodolist_repository_delete(
    params: Mapping[str, Any], todolist_repository: AbstractTodoListRepository
):
    repo = todolist_repository
    todo = await repo.list()
    await repo.remove(TodoListItem(id=params["todolist"][1].id, label="Write code"))
    todo = await repo.list()
    assert todo == [
        params["todolist"][0],
        params["todolist"][2],
    ]
