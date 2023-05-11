from pydantic import BaseSettings


class Settings(BaseSettings):
    # Jinja2 config
    template_search_path: str = "todolist:templates"

    # HTTP server Config
    bind: str = "0.0.0.0:8000"
    use_reloader: bool = False

    class Config:  # type: ignore
        env_prefix = "todolist_"
