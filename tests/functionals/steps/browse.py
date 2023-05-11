from typing import Any

from behave import when  # type: ignore


@when('I visit "{path}"')
def i_visit(context: Any, path: str):
    context.browser.get(path)
