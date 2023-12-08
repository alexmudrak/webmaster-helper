from rest_framework import serializers

from api.abstract.serializers import AbstractSerializer
from api.mail_box.serializers import MailSettingsLinkedSerializer
from api.user.models import User


class UserSerializer(AbstractSerializer):
    mail_settings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "mail_settings",
            "created",
            "updated",
        ]
        read_only_field = ["is_active", "email"]

    def get_mail_settings(self, obj):
        mail_settings_instance = obj.mail_settings.filter(project=None).first()

        if mail_settings_instance:
            mail_settings_serializer = MailSettingsLinkedSerializer(
                mail_settings_instance
            )
            return mail_settings_serializer.data
        else:
            return None
