from typing import Annotated

from fastapi import Response

from todolist.adapters.fastapi import (
    Templatizer,
    FastAPIConfigurator,
    templatize,
    configure,
)
from todolist.domain.model import TodoListItem


async def todolist(
    templatize: Annotated[Templatizer, templatize("todolist.jinja2")],
) -> Response:
    todo = [TodoListItem(label="Buy some milk")]
    return await templatize(todolist=todo)


@configure
def includeme(app: FastAPIConfigurator) -> None:
    app.add_api_route("/components/todo-list", todolist, methods=["GET"])
