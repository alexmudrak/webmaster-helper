from celery import shared_task
from django.utils.timezone import timedelta

from api.project.models import Project
from mail.client import MailApp
from mail.models import Mail, MailSettings
from utils.logger_handler import get_logger

logger = get_logger(__name__)


@shared_task
def get_mails(settings_id: int):
    # TODO: Add documentation
    settings = MailSettings.objects.filter(id=settings_id).first()

    start_collect_date = None
    last_receive_mail = Mail.objects.filter(mail_settings=settings)
    if last_receive_mail:
        last_date = last_receive_mail.latest("receive_date").receive_date
        start_collect_date = last_date - timedelta(days=3)

    mail_app = MailApp(settings)

    logger.info(f"Start collecting mails for {settings.smtp_username}")
    mail_app.start_collect_mail_messages(start_collect_date)

    settings.check_status = "DONE"
    settings.save()
    logger.info(f"Finish collecting mails for {settings.smtp_username}")


@shared_task
def send_mails(project_id: int, settings_id: int, mail_data: dict):
    settings = MailSettings.objects.filter(id=settings_id).first()
    project = Project.objects.filter(id=project_id).first()
    mail_app = MailApp(settings)
    logger.info(f"Start sending mail for {settings.smtp_username}")
    mail_app.start_send_mail(
        subject=mail_data["subject"],
        to_email=mail_data["recipient"],
        body=mail_data["message"],
        project=project,
    )
    logger.info(f"Finish sending mail for {settings.smtp_username}")
