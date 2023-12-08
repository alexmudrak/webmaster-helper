from typing import Any

from django.db import IntegrityError, models

from api.abstract.models import AbstarctManager, AbstractModel
from api.url.models import Url
from utils.logger_handler import get_logger

logger = get_logger(__name__)


class SeoDataManager(AbstarctManager):
    def create_from_results(
        self, url_obj: Url, results: dict[Any, Any]
    ) -> None:
        seo_data_list = []

        for result_type, result_data in results.items():
            seo_data = self.model(
                url=url_obj,
                type=result_type,
                data=result_data,
            )
            seo_data_list.append(seo_data)

        try:
            self.model.objects.bulk_create(seo_data_list)
        except IntegrityError as error:
            logger.error(f"IntegrityError for {url_obj.url}. {error}")
        except Exception as error:
            logger.critical(f"Unknown error for {url_obj.url}. {error}")


class SeoData(AbstractModel):
    url = models.ForeignKey(
        to="url.Url",
        related_name="seo_data",
        on_delete=models.SET_NULL,
        null=True,
    )
    type = models.CharField(max_length=255, default="")
    data = models.JSONField()

    objects = SeoDataManager()

    def __str__(self):
        return f"SeoData for <{self.url}>"

    class Meta:
        db_table = "seo_data"
