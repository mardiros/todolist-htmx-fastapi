from fastapi import FastAPI

import todolist.ui.index
from todolist.adapters.fastapi import FastAPIConfigurator
from todolist.config import Settings


def configure(configurator: FastAPIConfigurator) -> None:
    configurator.scan(todolist.ui.index, categories=["fastapi"])


async def bootstrap(settings: Settings) -> FastAPI:
    with FastAPIConfigurator(settings) as configurator:
        configure(configurator)

    app = configurator.app

    return app
