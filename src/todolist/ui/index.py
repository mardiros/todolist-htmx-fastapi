from typing import Annotated

import pkg_resources
from fastapi import Response
from fastapi.staticfiles import StaticFiles

from todolist.adapters.fastapi import (
    FastAPIConfigurator,
    Templatizer,
    configure,
    templatize,
)


def serve_statics(app: FastAPIConfigurator) -> None:
    path = pkg_resources.resource_filename(
        *app.config.settings.static_path.split(":", 2)
    )
    app.mount("/static", StaticFiles(directory=path), name="static")


async def serve_index(
    templatize: Annotated[Templatizer, templatize("index.jinja2")],
) -> Response:
    return await templatize()


@configure
def includeme(app: FastAPIConfigurator) -> None:
    app.add_api_route("/", serve_index, methods=["GET"])
    serve_statics(app)
