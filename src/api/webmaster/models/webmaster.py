from django.db import models

from api.abstract.models import AbstractModel
from api.webmaster.manager import WebmasterManager


class Webmaster(AbstractModel):
    owner = models.ForeignKey(
        to="user.User",
        related_name="webmaster",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    objects = WebmasterManager()

    def __str__(self):
        return f"{self.name} <{self.owner.username}>"

    class Meta:
        db_table = "webmasters"
