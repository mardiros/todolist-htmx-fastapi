from pydantic import BaseSettings

from todolist.service.unit_of_work import AbstractUnitOfWork


class Settings(BaseSettings):
    # Jinja2 config
    template_search_path: str = "todolist.ui:templates"

    # Static dir
    static_path: str = "todolist.ui:static"

    # HTTP server Config
    bind: str = "0.0.0.0:8000"
    use_reloader: bool = False

    uow: AbstractUnitOfWork | str = ""

    class Config:  # type: ignore
        env_prefix = "todolist_"
