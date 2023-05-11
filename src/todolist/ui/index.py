from typing import Annotated

from fastapi import Response

from todolist.adapters.fastapi import (
    FastAPIConfigurator,
    Templatizer,
    configure,
    templatize,
)


async def serve_index(
    templatize: Annotated[Templatizer, templatize("index.jinja2")],
) -> Response:
    return await templatize()


@configure
def includeme(app: FastAPIConfigurator) -> None:
    app.add_api_route("/", serve_index, methods=["GET"])
