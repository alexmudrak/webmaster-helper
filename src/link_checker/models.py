from django.db import models

from api.abstract.models import AbstarctManager, AbstractModel


class LinkCheckManager(AbstarctManager):
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)


class LinkCheck(AbstractModel):
    link = models.ForeignKey(
        to="webmaster.PublishPage", on_delete=models.CASCADE
    )
    url = models.CharField(max_length=255, null=True)
    anchor = models.CharField(max_length=255, null=True)
    published = models.BooleanField(default=False)

    objects = LinkCheckManager()

    def __str__(self):
        return f"{self.link} <{self.published}>"

    class Meta:
        db_table = "link_checks"
