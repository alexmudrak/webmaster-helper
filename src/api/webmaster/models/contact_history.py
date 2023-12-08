from django.db import models

from api.abstract.models import AbstractModel
from api.webmaster.manager import WebmasterManager


class ContactHistory(AbstractModel):
    owner = models.ForeignKey(
        to="user.User",
        related_name="contact_history",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    webmaster = models.ForeignKey(
        to="webmaster.Webmaster",
        related_name="contact_history",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    website = models.ForeignKey(
        to="webmaster.Website",
        related_name="contact_history",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contact = models.ForeignKey(
        to="webmaster.Contact",
        related_name="contact_history",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        to="project.Project",
        related_name="contact_history",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    subject = models.CharField()
    body = models.TextField()

    objects = WebmasterManager()

    def __str__(self):
        return f"{self.contact}"

    class Meta:
        db_table = "contacts_history"
