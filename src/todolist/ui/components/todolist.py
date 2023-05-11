from typing import Annotated

from fastapi import Response

from todolist.adapters.fastapi import (
    FastAPIConfigurator,
    FastConfig,
    Templatizer,
    configure,
    templatize,
)


async def todolist(
    app: FastConfig,
    templatize: Annotated[Templatizer, templatize("todolist.jinja2")],
) -> Response:
    async with app.uow as uow:
        todo = await app.uow.todolist.list()
        await uow.rollback()
    return await templatize(todolist=todo)


@configure
def includeme(app: FastAPIConfigurator) -> None:
    app.add_api_route("/components/todo-list", todolist, methods=["GET"])
