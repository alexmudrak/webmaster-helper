from api.abstract.serializers import AbstractSerializer
from api.project.serializers import ProjectSerializer
from api.url.serializers import UrlSerializer
from api.webmaster.models.publish_page import PublishPage


class PublishPageSerializer(AbstractSerializer):
    project = ProjectSerializer()
    website = UrlSerializer()

    class Meta:
        model = PublishPage
        fields = [
            "id",
            "project",
            "website",
            "url",
        ]
