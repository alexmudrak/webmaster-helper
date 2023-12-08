from django.db.models import Sum
from rest_framework import serializers

from api.abstract.serializers import AbstractSerializer
from api.mail_box.serializers import MailSettingsLinkedSerializer
from api.project.models import Project
from api.url.serializers import UrlSerializer


class ProjectLessSerializer(AbstractSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]


class ProjectSerializer(AbstractSerializer):
    url = UrlSerializer(required=False)
    published_count = serializers.SerializerMethodField(read_only=True)
    total_spend = serializers.SerializerMethodField(read_only=True)
    last_published_date = serializers.SerializerMethodField(read_only=True)

    mail_settings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "url",
            "published_count",
            "total_spend",
            "created",
            "last_published_date",
            "mail_settings",
        ]

    def get_published_count(self, obj):
        if hasattr(obj, "publish_page"):
            field_instances = obj.publish_page.filter(
                project=obj,
            )
            if field_instances:
                return len(field_instances)
        return 0

    def get_total_spend(self, obj):
        if hasattr(obj, "payment_history"):
            total_spend = obj.payment_history.filter(
                project=obj,
            ).aggregate(
                total=Sum("price")
            )["total"]
            return total_spend if total_spend is not None else 0

        return 0

    def get_last_published_date(self, obj):
        if hasattr(obj, "publish_page"):
            latest_publish_page = (
                obj.publish_page.filter(
                    project=obj,
                )
                .order_by("-publish_date")
                .first()
            )
            if latest_publish_page:
                return latest_publish_page.publish_date
            return None

    def get_mail_settings(self, obj):
        if hasattr(obj, "mail_settings"):
            mail_settings_instance = obj.mail_settings.filter(
                project=obj,
            ).first()

            if mail_settings_instance:
                mail_settings_serializer = MailSettingsLinkedSerializer(
                    mail_settings_instance
                )
                return mail_settings_serializer.data
        return None
