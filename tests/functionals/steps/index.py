from typing import Any

from behave import given  # type: ignore


@given("anonymous user on the index page")
def start_fastcms(context: Any):
    context.browser.get("/")
