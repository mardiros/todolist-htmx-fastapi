from typing import Annotated, Any, Callable, Coroutine

from fastapi import Depends, Response

from todolist.adapters.fastapi import (
    AppConfig,
    FastAPIConfigurator,
    FastConfig,
    configure,
)

Parametrizer = Coroutine[Any, Any, Response]
Templatizer = Callable[..., Parametrizer]
TemplateEngine = Callable[[AppConfig], Templatizer]


def jinja2resp(template: str) -> TemplateEngine:
    def templatizer(app: FastConfig) -> Templatizer:
        async def parametrizer(**kwargs: Any) -> Response:
            data = await app.renderer.render(template, **kwargs)
            return Response(data)

        return parametrizer

    return templatizer


def templatize(template: str) -> TemplateEngine:
    return Depends(jinja2resp(template))


async def serve_index(
    templatize: Annotated[Templatizer, templatize("index.jinja2")],
) -> Response:
    return await templatize()


@configure
def includeme(app: FastAPIConfigurator) -> None:
    app.add_api_route("/", serve_index, methods=["GET"])
