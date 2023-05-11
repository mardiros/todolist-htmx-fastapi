import time
from typing import Any

from behave import given, then, when  # type: ignore


@given("I wait")
@when("I wait")
@then("I wait")
def i_wait(context: Any):
    time.sleep(60 * 5)
