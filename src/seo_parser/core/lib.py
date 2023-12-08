from abc import ABC, abstractmethod
from typing import Any

from httpx import ReadTimeout
from playwright.sync_api import Error, Page, Response, TimeoutError

from utils.browser_client import BrowserClient
from utils.logger_handler import get_logger
from utils.request_client import RequestClient

logger = get_logger(__name__)


# TODO: Need to delete all Any | None typing


class AbstractSeoSite(ABC):
    name: str
    url: str
    validate_element: str
    single_json_var: bool | str
    multi_json_var: bool | dict[str, str]
    value: dict | str | int | float | None
    serialize_data: dict[str, Any]
    captcha: str | None
    parse_method: str

    # TODO: Write documentation for all fields and
    # method logic

    @abstractmethod
    def __init__(
        self,
        browser_client: BrowserClient | None = None,
        request_client: RequestClient | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def serialize(self):
        raise NotImplementedError

    @abstractmethod
    def parse_data(self, url: str):
        raise NotImplementedError


class SeoSite(AbstractSeoSite):
    value = None

    def __init__(
        self,
        browser_client: BrowserClient | None = None,
        request_client: RequestClient | None = None,
    ):
        self.browser_client = browser_client
        self.request_client = request_client

    def get_value(self) -> dict | None:
        if isinstance(self.page, Page):
            if self.single_json_var and isinstance(self.single_json_var, str):
                return self.page.evaluate(self.single_json_var)
            if self.multi_json_var and isinstance(self.multi_json_var, dict):
                collect_values = {}
                for name, variable in self.multi_json_var.items():
                    collect_values[name] = self.page.locator(
                        variable
                    ).inner_text()
                return collect_values
        return None

    def __check_captha(self, response: Response | None) -> bool:
        for captcha in [self.captcha or "captcha", "captcha"]:
            if response and captcha in response.text():
                raise NotImplementedError(
                    "Need to implement anti captcha method!"
                )
        # TODO: Need for Moz CF bypass
        if isinstance(self.page, Page) and self.name == "Moz":
            self.page.reload()
        return True

    def serialize(self) -> dict:
        # TODO: Create dataclass for result
        if self.value:
            self.serialize_data["values"] = {"value": self.value}
        return self.serialize_data

    def _test_page(self, name: str):
        # This is function for debugging
        screenshot_path = f"{name}-screenshot.png"
        self.page.screenshot(path=screenshot_path)

        logger.debug(f"Screenshot saved to: {screenshot_path}")

        # Get the HTML content of the page
        html_content = self.page.content()
        html_path = f"{name}-page.html"
        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        logger.debug(f"HTML content saved to: {html_path}")

    def parse_data_browser(self, url: str) -> "SeoSite":
        if self.browser_client:
            self.page = self.browser_client.get_client
            self.page.set_extra_http_headers(
                {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/58.0.3029.110 Safari/537.3"
                    )
                }
            )

            try:
                logger.info(f"Trying to get data from {self.url + url}")
                response = self.page.goto(self.url + url)
            except Error as error:
                # TODO: Probably need to implement state
                #       for this implementation to SeoDataSite
                logger.info(
                    f"Trying to get data from {self.url + url} "
                    f"after exception: {error}"
                )
                self.page = self.browser_client.get_client_without_proxy
                response = self.page.goto(self.url + url)

            self.page.evaluate(
                """() => {
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
    });
}"""
            )
            self.page.mouse.move(100, 100)
            # self._test_page("debug")

            self.__check_captha(response)
            validate = self.page.locator(f"xpath={self.validate_element}")
            if validate.is_enabled():
                self.value = self.get_value()

        return self

    def parse_data_request(self, url: str) -> "SeoSite":
        if self.request_client:
            self.page = self.request_client.get_client
            response = self.page.get(self.url + url)
            self.value = response.text if response.status_code == 200 else None
        return self

    def parse_data(self, url: str) -> dict:
        self.value = None
        try:
            logger.info(f"Trying parse data `{self.parse_method}` in {url}")
            if self.parse_method == "browser":
                return self.parse_data_browser(url).serialize()
            if self.parse_method == "request":
                return self.parse_data_request(url).serialize()
        except (TimeoutError, NotImplementedError, ReadTimeout) as error:
            logger.error(f"Timeout error for {url} - {error}")
            self.serialize_data.setdefault("values", {})[
                "error"
            ] = f"Collect error - {error}"
        except Error as error:
            logger.critical(f"Critical error for {url} - {error}")
            match error.message:
                case _ if "ERR_TUNNEL_CONNECTION_FAILED" in error.message:
                    error_message = "Can't get tunnel to the site"
                case _:
                    error_message = "Unknown `Error`"
            self.serialize_data.setdefault("values", {})[
                "error"
            ] = f"Collect error - {error_message}"
        return self.serialize()
