from urllib.parse import urlparse

from django.db import models
from django.shortcuts import get_object_or_404

from api.abstract.models import AbstarctManager, AbstractModel


class UrlManager(AbstarctManager):
    def get_object_by_domain(self, domain: str):
        return get_object_or_404(self.model, url__contains=domain)


class Url(AbstractModel):
    url = models.URLField(max_length=255, unique=True)
    # TODO: add enum
    seo_status = models.CharField(max_length=255, null=True, default="DONE")

    objects = UrlManager()

    def __str__(self):
        return f"{self.url}"

    @property
    def domain(self):
        parsed_url = urlparse(str(self.url))
        return parsed_url.netloc

    class Meta:
        db_table = "urls"
