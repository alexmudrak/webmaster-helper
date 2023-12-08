import os

from playwright.sync_api import Page, sync_playwright
from playwright_stealth import stealth_sync


class BrowserClient:
    # TODO: Write documentations
    def __init__(self, *args, **kwargs):
        self.headless = kwargs.get("headless", True)
        self.proxy = kwargs.get("use_proxy", False)
        self.proxy_server = os.getenv("PROXY_SERVER", None)
        self.proxy_username = os.getenv("PROXY_USERNAME", None)
        self.proxy_password = os.getenv("PROXY_PASSWORD", None)
        self.playwright = sync_playwright().start()

    def __enter__(self) -> "BrowserClient":
        proxy_data = {}
        if all(
            (
                self.proxy,
                self.proxy_server,
                self.proxy_username,
                self.proxy_password,
            )
        ):
            proxy_data["server"] = self.proxy_server
            proxy_data["username"] = self.proxy_username
            proxy_data["password"] = self.proxy_password

        self.client = self.playwright.chromium.launch(
            headless=self.headless,
            proxy=proxy_data or None,
            handle_sigint=False,
            handle_sigterm=False,
            handle_sighup=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        return self

    @property
    def get_client(self) -> Page:
        page = self.client.new_page()
        stealth_sync(page)
        return page

    @property
    def get_client_without_proxy(self) -> Page:
        browser = self.playwright.chromium.launch(
            headless=self.headless,
            proxy=None,
        )
        context = browser.new_context()
        page = context.new_page()
        stealth_sync(page)
        return page

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.client.close()
        self.playwright.stop()
