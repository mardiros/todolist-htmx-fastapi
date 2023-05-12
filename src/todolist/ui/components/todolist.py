from typing import Annotated

from fastapi import Form, Response

from todolist.adapters.fastapi import (
    FastAPIConfigurator,
    FastConfig,
    Templatizer,
    configure,
    templatize,
)
from todolist.domain.model import TodoListItem


async def todolist(
    app: FastConfig,
    templatize: Annotated[Templatizer, templatize("todolist.jinja2")],
) -> Response:
    async with app.uow as uow:
        todo = await app.uow.todolist.list()
        await uow.rollback()
    return await templatize(todolist=todo)


async def new_item(
    app: FastConfig,
    templatize: Annotated[Templatizer, templatize("new_item.jinja2")],
) -> Response:
    return await templatize()


async def create_item(
    app: FastConfig,
    label: Annotated[str, Form()],
    templatize: Annotated[Templatizer, templatize("new_item.jinja2")],
) -> Response:
    item = TodoListItem(label=label)
    async with app.uow as uow:
        await app.uow.todolist.add(item)
        await uow.commit()
    ret = await templatize()
    ret.headers.append("HX-Trigger", "reload-todo-list")
    return ret


async def delete_item(app: FastConfig, item_id: str) -> Response:
    async with app.uow as uow:
        await uow.todolist.remove(TodoListItem(id=item_id, label="xxx"))
    return Response("", status_code=204, headers={"HX-Trigger": "reload-todo-list"})


@configure
def includeme(app: FastAPIConfigurator) -> None:
    app.add_api_route("/components/todo-list", todolist, methods=["GET"])
    app.add_api_route("/components/todo-list/new", new_item, methods=["GET"])
    app.add_api_route("/components/todo-list", create_item, methods=["POST"])
    app.add_api_route(
        "/components/todo-list/{item_id}", delete_item, methods=["DELETE"]
    )
