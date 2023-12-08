from django.db import models

from api.abstract.models import AbstractModel
from api.webmaster.manager import WebmasterManager


class Contact(AbstractModel):
    owner = models.ForeignKey(
        to="user.User",
        on_delete=models.CASCADE,
        default="",
        related_name="contact",
    )
    # TODO: add enum types for contacts
    type = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, default="")
    webmaster = models.ForeignKey(
        to="webmaster.Webmaster",
        on_delete=models.CASCADE,
        related_name="contact",
    )

    objects = WebmasterManager()

    def __str__(self):
        return f"{self.webmaster.name} <{self.type} : {self.contact}>"

    class Meta:
        db_table = "contacts"
