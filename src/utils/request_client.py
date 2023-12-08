import os

import httpx
from fake_useragent import UserAgent


class RequestClient:
    # TODO: Write documentations
    def __init__(self, *args, **kwargs):
        self.headers = kwargs.get("headers", False)
        self.proxy = kwargs.get("use_proxy", False)
        self.proxy_server = os.getenv("PROXY_SERVER", None)
        self.proxy_username = os.getenv("PROXY_USERNAME", None)
        self.proxy_password = os.getenv("PROXY_PASSWORD", None)

    def __enter__(self) -> "RequestClient":
        proxy_data = {}
        if all(
            (
                self.proxy,
                self.proxy_server,
                self.proxy_username,
                self.proxy_password,
            )
        ):
            proxy_data["all://"] = (
                f"http://{self.proxy_username}:{self.proxy_password}"
                f"@{self.proxy_server}"
            )

        if not self.headers:
            self.headers = {
                "accept": (
                    "text/html,application/xhtml+xml,application/xml;"
                    "q=0.9,image/avif,image/webp,image/apng,*/*;"
                    "q=0.8,application/signed-exchange;v=b3;q=0.9"
                ),
                "user-agent": UserAgent().random,
                "Accept-Language": "en-US;q=0.8,ru-RU,ru;q=0.5,en;q=0.3",
            }

        self.client = httpx.Client(
            proxies=proxy_data or None,
            headers=self.headers,
            timeout=10.0,
        )
        return self

    @property
    def get_client(self) -> httpx.Client:
        return self.client

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.client.close()
