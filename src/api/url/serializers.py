from urllib.parse import urlparse

from api.abstract.serializers import AbstractSerializer
from api.url.models import Url


class UrlSerializer(AbstractSerializer):
    class Meta:
        model = Url
        fields = [
            "id",
            "url",
            "seo_status",
        ]

    def validate_url(self, value: str):
        parsed_url = urlparse(value)
        return f"{parsed_url.scheme}://{parsed_url.netloc}".lower()
