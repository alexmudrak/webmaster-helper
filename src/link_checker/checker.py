import urllib
from urllib.parse import urlparse

from httpx import ProxyError
from lxml.html import fromstring

from api.webmaster.models.publish_page import PublishPage
from link_checker.models import LinkCheck
from utils.logger_handler import get_logger
from utils.request_client import RequestClient

logger = get_logger(__name__)


def start_checker(publish_page: PublishPage) -> int:
    # TODO: Add documentation
    url = publish_page.project.url.domain
    page = publish_page.url

    if not urlparse(page).scheme:
        page = f"{urlparse(url).scheme}://{page}"
    with RequestClient(use_proxy=True) as request:
        try:
            logger.info(f"Trying to get information from: {page} for {url}")
            response = request.get_client.get(page, follow_redirects=True)
            soup = fromstring(response.text)
            elements = soup.xpath(f"//a[contains(@href, '{url}')]")

            logger.info(f"On page: {page} find {len(elements)} for {url}")
            if len(elements) > 0:
                for element in elements:
                    LinkCheck.objects.create(
                        link=publish_page,
                        url=urllib.parse.unquote(element.get("href")),
                        anchor=element.text,
                        published=True,
                    )
            else:
                LinkCheck.objects.create(
                    link=publish_page, url=None, anchor=None
                )
            logger.info(
                f"For page: {page} LinkCheck was created - {publish_page}"
            )
            return len(elements)
        except ProxyError as error:
            logger.error(f"For page: {page}. Error: {error}")
            return 0
