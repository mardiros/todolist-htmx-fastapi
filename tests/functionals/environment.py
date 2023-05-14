from collections import defaultdict
from typing import Any

from behave import use_fixture  # type: ignore
from fixtures import browser, todolist  # type: ignore


def before_scenario(context: Any, scenario: Any):
    port = 6556
    context.stash = defaultdict(dict)
    use_fixture(todolist, context, port=port)
    use_fixture(browser, context, port=port)
    context.endpoint = f"http://localhost:{port}"
