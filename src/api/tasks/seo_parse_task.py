from celery import shared_task
from django.utils import timezone

from api.url.models import Url
from seo_parser.parser import start_parser
from utils.logger_handler import get_logger

logger = get_logger(__name__)


@shared_task
def get_seo_metrics(url_id: str) -> None:
    """This function collect all seo metrics for Url and
    store it in `seo_data` table."""
    url = Url.objects.filter(id=url_id).first()

    # TODO: Check the date of the last parsing, if it's less than
    # 3 days ago, then don't collect data. This should not be
    # considered if the execution is via force_start.

    logger.info(f"Start collect SEO data for `{url}`.")
    start_parser(url)

    url.seo_check_status = "DONE"
    url.seo_check_date = timezone.now()
    url.save()
    logger.info(f"Finish collect SEO data for `{url}`.")
