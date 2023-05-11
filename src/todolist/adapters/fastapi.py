import logging
from typing import Annotated, Any, Callable, Coroutine, Type

import venusian  # type: ignore
from fastapi import Depends, FastAPI, Response
from fastapi.routing import APIRouter
from starlette.types import ASGIApp

from todolist.adapters.jinja2 import Jinja2TemplateRender
from todolist.config import Settings

log = logging.getLogger(__name__)


def configure(
    wrapped: Callable[["FastAPIConfigurator"], None]
) -> Callable[["FastAPIConfigurator"], None]:
    """Decorator used to attach route in a submodule while using the confirator.scan"""

    def callback(
        scanner: venusian.Scanner, name: str, ob: Callable[[venusian.Scanner], None]
    ) -> None:
        if not isinstance(scanner, FastAPIConfigurator):
            return  # coverage: ignore
        ob(scanner)

    venusian.attach(wrapped, callback, category="fastapi")
    return wrapped


class AppConfig:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.renderer = Jinja2TemplateRender(settings.template_search_path)


class FastAPIConfigurator(venusian.Scanner):
    app: FastAPI
    config: AppConfig

    def __init__(self, settings: Settings):
        FastAPIConfigurator.config = AppConfig(settings)
        super().__init__(
            app=FastAPI(docs_url=None, redoc_url=None),
        )

    def __enter__(self) -> "FastAPIConfigurator":
        return self

    def __exit__(
        self,
        exception_type: Type[Exception],
        exception_value: Exception,
        exception_traceback: Any,
    ) -> None:
        log.warning("Exiting")
        if exception_value:
            log.error(  # coverage: ignore
                "Unexpected exception while existing: %r" % (exception_value),
                exc_info=exception_traceback,
            )

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Coroutine[Any, Any, Response]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.app.add_api_route(path, endpoint, *args, **kwargs)

    def include_router(self, router: APIRouter, *args: Any, **kwargs: Any) -> None:
        self.app.include_router(router, *args, **kwargs)

    def mount(self, path: str, app: ASGIApp, name: str) -> None:
        self.app.mount(path, app, name)


FastConfig = Annotated[AppConfig, Depends(lambda: FastAPIConfigurator.config)]
