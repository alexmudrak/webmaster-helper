from django.db import models

from api.abstract.models import AbstractModel
from api.webmaster.manager import WebmasterManager


class Website(AbstractModel):
    owner = models.ForeignKey(
        to="user.User",
        related_name="websites",
        on_delete=models.CASCADE,
    )
    webmaster = models.ManyToManyField(
        to="webmaster.Webmaster",
        related_name="websites",
        blank=True,
    )
    url = models.ForeignKey(
        to="url.Url",
        related_name="websites",
        on_delete=models.CASCADE,
        null=True,
    )
    publish_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    information = models.TextField(
        null=True,
        blank=True,
    )

    objects = WebmasterManager()

    def __str__(self):
        return f"{self.url} - {self.owner}"

    class Meta:
        unique_together = ("owner", "url")
        db_table = "websites"
