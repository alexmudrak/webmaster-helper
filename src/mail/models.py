from django.db import IntegrityError, models
from django.utils import timezone

from api.abstract.models import AbstarctManager, AbstractModel
from utils.logger_handler import get_logger
from utils.types import MailMessage

logger = get_logger(__name__)


class MailManager(AbstarctManager):
    def create_message(self, result: MailMessage) -> None:
        if isinstance(result, MailMessage):
            try:
                self.create(
                    mail_settings=result.mail_settings,
                    mail_box=result.mail_box,
                    mail_id=result.mail_id,
                    replay_to=result.replay_to,
                    author_mail=result.author_mail,
                    author_name=result.author_name,
                    subject=result.subject,
                    body=result.body,
                    receive_date=result.receive_date,
                )
            except IntegrityError:
                logger.critical(
                    "IntegrityError occurred. Handling the error..."
                )

    def create_from_results(
        self,
        results: list[MailMessage] | None,
    ):
        if isinstance(results, list):
            for result in results:
                self.create_message(result)

    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)


class MailSettings(AbstractModel):
    owner = models.ForeignKey(
        to="user.User",
        related_name="mail_settings",
        on_delete=models.SET_NULL,
        null=True,
    )
    project = models.ForeignKey(
        to="project.Project",
        related_name="mail_settings",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    mail_folders = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    smtp_server = models.CharField(max_length=255, null=True)
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_username = models.CharField(max_length=255)
    smtp_password = models.CharField(max_length=255)
    imap_ssl = models.BooleanField(default=False)
    imap_server = models.CharField(max_length=255)
    imap_port = models.PositiveIntegerField(default=143)
    imap_username = models.CharField(max_length=255)
    imap_password = models.CharField(max_length=255)
    check_date = models.DateTimeField(default=timezone.now)
    check_status = models.CharField(max_length=255, null=True, default="DONE")

    objects = MailManager()

    def __str__(self):
        return f"Mail Setting {self.owner} <{self.project}>"

    class Meta:
        unique_together = ("owner", "project")
        db_table = "mail_settings"


class Mail(AbstractModel):
    mail_settings = models.ForeignKey(
        to="mail.MailSettings",
        related_name="mail",
        on_delete=models.SET_NULL,
        null=True,
    )
    mail_box = models.CharField(max_length=255, null=True)
    mail_id = models.CharField(max_length=512, unique=True)
    replay_to = models.CharField(max_length=512, null=True, default=None)
    author_name = models.CharField(max_length=255)
    author_mail = models.EmailField()
    subject = models.CharField(max_length=512)
    body = models.TextField()
    receive_date = models.DateTimeField()

    objects = MailManager()

    def __str__(self):
        return f"Mail from {self.author_mail} with subject: {self.subject}"

    class Meta:
        unique_together = ("mail_settings", "mail_id")
        db_table = "mails"
