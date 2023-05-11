from typing import Any

import pkg_resources
from jinja2 import Environment, FileSystemLoader, Template


def build_searchpath(template_search_path: str) -> list[str]:
    searchpath: list[str] = []
    paths = template_search_path.split(",")
    for path in paths:
        if ":" in path:
            searchpath.append(pkg_resources.resource_filename(*path.split(":", 2)))
        else:
            searchpath.append(path)
    return searchpath


class Jinja2TemplateRender:
    def __init__(self, template_search_path: str) -> None:
        super().__init__()
        self.env = Environment(
            loader=FileSystemLoader(build_searchpath(template_search_path)),
            enable_async=True,
        )

    def get_template(self, template: str) -> Template:
        return self.env.get_template(
            template,
            globals={},
        )

    async def render(self, template: str, **kwargs: Any) -> str:
        tpl = self.get_template(template)
        ret = await tpl.render_async(**kwargs)
        return ret
