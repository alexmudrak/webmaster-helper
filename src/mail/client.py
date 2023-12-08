from datetime import datetime

from api.project.models import Project
from mail.models import Mail, MailSettings
from utils.mail_client import MailClient


class MailApp:
    def __init__(self, settings: MailSettings):
        self.settings = settings
        self.client = MailClient(
            smtp_server=str(self.settings.smtp_server),
            smtp_port=int(self.settings.smtp_port),
            smtp_username=str(self.settings.smtp_username),
            smtp_password=str(self.settings.smtp_password),
            imap_ssl=bool(self.settings.imap_ssl),
            imap_server=str(self.settings.imap_server),
            imap_port=int(self.settings.imap_port),
            imap_username=str(self.settings.imap_username),
            imap_password=str(self.settings.imap_password),
        )

    def start_collect_mail_messages(
        self,
        start_date_collect: datetime | None = None,
    ) -> None:
        account_name = self.client.smtp_username or self.client.imap_username

        self.client.get_emails(
            username=str(account_name),
            settings=self.settings,
            start_date=start_date_collect,
        )

    def start_send_mail(
        self,
        subject: str,
        to_email: str,
        body: str,
        project: Project,
        mail: Mail | None = None,
    ):
        settings = self.settings
        self.client.send_email(
            subject,
            to_email,
            body,
            settings,
            project,
            mail,
        )
