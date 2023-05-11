import json
import os
import time
import uuid
from multiprocessing import Process
from pathlib import Path
from typing import Any, Callable, Iterator, List, Optional

from behave import fixture  # type: ignore
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.remote.webelement import WebElement

from todolist.entrypoint import main


class Browser:
    def __init__(self, web_root: str) -> None:
        self.browser = Firefox()
        self.web_root = web_root

        self.db_name = "todolist"
        self.db_version = 1

    def wait_for(
        self,
        method: Callable[..., Any],
        *args: Any,
        timeout: int = 10,
        interval: float = 0.2,
    ):
        start_time = time.time()
        while True:
            try:
                return method(*args)
            except (AssertionError, WebDriverException) as exc:
                if time.time() - start_time > timeout:
                    raise exc
                time.sleep(interval)

    def find_element_by_xpath(self, path: str) -> WebElement:
        return self.wait_for(
            self.browser.find_element,  # type: ignore
            By.XPATH,
            path,
        )

    def dont_find_element_by_xpath(self, path: str) -> None:
        try:
            self.browser.find_element(By.XPATH, path)
        except NoSuchElementException:
            return
        else:
            raise ValueError(f"Element {path} exists")

    def find_elements_by_xpath(self, path: str) -> List[WebElement]:
        return self.wait_for(
            self.browser.find_elements,  # type: ignore
            By.XPATH,
            path,
        )

    def get(self, path: str):
        if path.startswith("/"):
            self.browser.get(f"{self.web_root}{path}")
        else:
            self.browser.get(f"{path}")

    def quit(self):
        self.browser.quit()

    def get_index_db_value(self, table_name: str, key: str) -> Optional[Any]:
        log_id = uuid.uuid1().hex
        self.browser.execute_script(
            """
            var [
                dbName, dbVersion, tableName, searchKey, logId
            ] = [
                arguments[0], arguments[1], arguments[2], arguments[3], arguments[4]
            ];

            var request = window.indexedDB.open(dbName, dbVersion);
            request.onsuccess = function(event) {
                var db = event.target.result;
                var req = db.transaction(
                    tableName, 'readwrite'
                ).objectStore(tableName).get(searchKey)
                req.onsuccess = function(event) {
                    debugNode = document.createElement("code");
                    debugNode.id = logId;
                    debugNode.innerText = JSON.stringify(event.target.result);
                    document.body.appendChild(debugNode);
                };
                req.onerror = function(event) {
                    console.log(event);
                };
            };
            request.onerror = function(event) {
                console.log(event);
            };
            """,
            self.db_name,
            self.db_version,
            table_name,
            key,
            log_id,
        )
        ret = self.wait_for(
            self.browser.find_element,  # type: ignore
            By.ID,
            log_id,
        )
        data = json.loads(ret.text)

        self.browser.execute_script(
            """
                var [ logId ] = [ arguments[0] ];

                debugNode = document.getElementById(logId);
                document.body.removeChild(debugNode)
            """,
            log_id,
        )
        return data

    def add_index_db_value(self, table_name: str, key: str, value: Any) -> None:
        self.browser.execute_script(
            """
            var [
                dbName, dbVersion, tableName, searchKey, targetValue
            ] = [
                arguments[0], arguments[1], arguments[2], arguments[3], arguments[4]
            ];
            var request = window.indexedDB.open(dbName, dbVersion);
            request.onsuccess = function(event) {
                var db = event.target.result;
                var objectStore = db.transaction(
                    tableName, 'readwrite'
                ).objectStore(tableName);
                var requestUpdate = objectStore.add(targetValue, searchKey);
                requestUpdate.onsuccess = function(event) {
                    db.commit;
                };
            };
            """,
            self.db_name,
            self.db_version,
            table_name,
            key,
            value,
        )

    def remove_target_blank(self, text: str) -> None:
        # xpath = f'//a[contains(text(), "{text}")]'

        # self.browser.execute_script("""
        # var el = document.evaluate(
        #     arguments[0],
        #     document,
        #     null,
        #     XPathResult.FIRST_ORDERED_NODE_TYPE,
        #     null
        # ).singleNodeValue;

        # el.setAttribute("target", "_self");
        # """,
        # xpath)

        self.browser.execute_script(
            """
        var els = document.getElementsByTagName("a");
        for (var i = 0; i < els.length; i++) {
            els[i].setAttribute("target", "_self");
        }
        """
        )


def run_server(port: int, **kwargs: Any):
    import sys

    p = (Path(__file__).parent.parent).resolve()
    sys.path.append(str(p))
    settings: dict[str, Any] = {"bind": f"localhost:{port}", **kwargs}
    os.environ.update({f"todolist_{k}": v for k, v in settings.items()})

    main()


@fixture
def todolist(context: Any, port: int, **kwargs: Any) -> Iterator[None]:
    proc = Process(target=run_server, args=(port,), daemon=True)
    proc.start()
    yield
    proc.kill()


@fixture
def browser(context: Any, port: int, **kwargs: Any) -> Iterator[None]:
    context.browser = Browser(f"http://localhost:{port}")
    yield
    context.browser.quit()


if __name__ == "__main__":
    run_server(6556, use_reloader="true")
