from django.conf import settings

from api.url.models import Url
from seo_parser.libs import seo_sites
from seo_parser.models import SeoData
from utils.browser_client import BrowserClient
from utils.logger_handler import get_logger
from utils.request_client import RequestClient

logger = get_logger(__name__)


def start_parser(url_obj: Url) -> None:
    # TODO: Add documentation
    with RequestClient(use_proxy=True) as request:
        with BrowserClient(
            headless=False if settings.DEBUG else True,
            use_proxy=True,
        ) as browser:
            results = [
                site(
                    browser_client=browser,
                    request_client=request,
                ).parse_data(url_obj.domain)
                for site in seo_sites
            ]
            logger.info(f"Parsed result for site `{url_obj}` - {results}.")
    data = {obj["db_table_name"]: obj["values"] for obj in results}
    SeoData.objects.create_from_results(url_obj, data)
