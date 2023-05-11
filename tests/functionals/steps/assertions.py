from typing import Any

from behave import then  # type: ignore
from hamcrest import assert_that, equal_to  # type: ignore

"""
Debug in the devtools of firefox

function getElementByXpath(path) {
  return document.evaluate(
    path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null
  ).singleNodeValue;
}
"""


@then('I see the text "{text}"')
def assert_text(context: Any, text: str):
    text = text.replace("'", "\\'")
    context.browser.find_element_by_xpath(
        f"//*[contains(text(), '{text}') or .='{text}']"
    )


@then('I don\'t see the text "{text}"')
def assert_not_text(context: Any, text: str):
    text = text.replace("'", "\\'")
    context.browser.dont_find_element_by_xpath(
        f"//*[contains(text(), '{text}') or .='{text}']"
    )


@then('I see the heading "{text}"')
def assert_h1(context: Any, text: str):
    context.browser.find_element_by_xpath(f"//h1[contains(text(), '{text}')]")


@then('I see the input "{placeholder}" contains "{text}"')
def assert_input(context: Any, placeholder: str, text: str):
    input = context.browser.find_element_by_xpath(
        f"//input[@placeholder='{placeholder}']"
    )
    assert_that(input.get_attribute("value"), equal_to(text))
