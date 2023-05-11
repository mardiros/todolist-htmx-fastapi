import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from todolist.bootstrap import bootstrap
from todolist.config import Settings


async def asyncmain(settings: Settings) -> None:
    config = Config()
    config.bind = settings.bind.split(",")
    config.use_reloader = settings.use_reloader
    app = await bootstrap(settings)
    await serve(app, config)  # type: ignore


def main() -> None:
    asyncio.run(asyncmain(Settings()))  # type: ignore


if __name__ == "__main__":
    main()
