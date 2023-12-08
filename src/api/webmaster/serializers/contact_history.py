from api.abstract.serializers import AbstractSerializer
from api.project.serializers import ProjectLessSerializer
from api.webmaster.models import ContactHistory
from api.webmaster.serializers.contact import ContactLessSerializer
from api.webmaster.serializers.webmaster import WebmasterLessSerializer
from api.webmaster.serializers.website import WebsiteLessSerializer


class ContactHistorySerializer(AbstractSerializer):
    webmaster = WebmasterLessSerializer(read_only=True)
    contact = ContactLessSerializer(read_only=True)
    project = ProjectLessSerializer(read_only=True)
    website = WebsiteLessSerializer(read_only=True)

    class Meta:
        model = ContactHistory
        fields = [
            "id",
            "subject",
            "body",
            "created",
            "webmaster",
            "contact",
            "project",
            "website",
        ]
