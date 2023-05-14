from typing import Any
from urllib.parse import urlencode

from behave import given  # type: ignore
from httpx import post


@given('an item "{label}"')
def add_todolist_item(context: Any, label: str):
    resp = post(
        f"{context.endpoint}/components/todo-list",
        content=urlencode({"label": label}),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200
