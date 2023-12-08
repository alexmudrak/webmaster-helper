from datetime import datetime

from celery import shared_task

from api.webmaster.models.publish_page import PublishPage
from link_checker.checker import start_checker
from utils.logger_handler import get_logger

logger = get_logger(__name__)


@shared_task
def get_link_check(page_id: str) -> None:
    """This function collect all seo metrics for Url and
    store it in `seo_data` table."""
    url = PublishPage.objects.filter(id=page_id).first()

    logger.info(f"Start check exist URL for `{url}`.")
    start_checker(url)

    url.check_status = "DONE"
    url.check_date = datetime.now()
    url.save()
    logger.info(f"Finish check exist URL for `{url}`.")
