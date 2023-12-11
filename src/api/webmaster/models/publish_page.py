from django.db import models
from django.utils import timezone

from api.abstract.models import AbstractModel
from api.webmaster.manager import WebmasterManager


class PublishPage(AbstractModel):
    website = models.ForeignKey(
        to="webmaster.Website",
        related_name="publish_page",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        to="project.Project",
        related_name="publish_page",
        on_delete=models.CASCADE,
    )
    payment = models.ForeignKey(
        to="webmaster.PaymentHistory",
        related_name="publish_page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    url = models.URLField(
        max_length=255,
        null=False,
    )
    publish_date = models.DateField(default=timezone.now)
    # TODO: Add enum for statuses
    check_date = models.DateField(null=True, blank=True)
    check_status = models.CharField(max_length=255, null=True, default=None)

    objects = WebmasterManager()

    def __str__(self):
        return f"{self.project.name} <{self.url}>"

    class Meta:
        unique_together = ("project", "url")
        db_table = "publish_page"
