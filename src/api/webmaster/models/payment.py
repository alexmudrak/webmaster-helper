from django.db import models

from api.abstract.models import AbstractModel
from api.webmaster.manager import WebmasterManager


class Payment(AbstractModel):
    class PaymentTypes(models.TextChoices):
        CARD = "Card"
        WEBMONEY = "Webmoney"
        YANDEX_MONEY = "Yandex money"
        OTHER = "Other"

    owner = models.ForeignKey(
        to="user.User",
        related_name="payment",
        on_delete=models.CASCADE,
    )
    webmaster = models.ForeignKey(
        to="webmaster.Webmaster",
        related_name="payment",
        on_delete=models.CASCADE,
        null=True,
    )
    type = models.CharField(
        choices=PaymentTypes.choices,
        default=PaymentTypes.OTHER,
    )
    details = models.CharField(
        max_length=255,
        null=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    objects = WebmasterManager()

    def __str__(self):
        return f"{self.webmaster.name} <{self.type} : {self.details}>"

    class Meta:
        db_table = "payments"
