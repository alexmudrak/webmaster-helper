from django.db import models

from api.abstract.models import AbstractModel
from api.webmaster.manager import WebmasterManager


class PaymentHistory(AbstractModel):
    owner = models.ForeignKey(
        to="user.User",
        related_name="payment_history",
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        to="project.Project",
        related_name="payment_history",
        on_delete=models.CASCADE,
        null=True,
    )
    website = models.ForeignKey(
        to="webmaster.Website",
        related_name="payment_history",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    payment = models.ForeignKey(
        to="webmaster.Payment",
        related_name="payment_history",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    objects = WebmasterManager()

    def __str__(self):
        return f"{self.payment}: {self.price}"

    class Meta:
        db_table = "payments_history"
