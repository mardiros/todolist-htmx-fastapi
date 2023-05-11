from fastapi import FastAPI

import todolist.ui.index
import todolist.ui.components.todolist
from todolist.adapters.fastapi import FastAPIConfigurator
from todolist.config import Settings


def configure(configurator: FastAPIConfigurator) -> None:
    configurator.scan(todolist.ui.index, categories=["fastapi"])
    configurator.scan(todolist.ui.components.todolist, categories=["fastapi"])


async def bootstrap(settings: Settings) -> FastAPI:
    with FastAPIConfigurator(settings) as configurator:
        configure(configurator)

    app = configurator.app

    return app
