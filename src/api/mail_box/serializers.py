from rest_framework import serializers

from api.abstract.serializers import AbstractSerializer
from mail.models import Mail, MailSettings


class MailBoxSerializer(AbstractSerializer):
    account_name = serializers.SerializerMethodField()

    class Meta:
        model = Mail
        # TODO: Need to handle body for teaser block
        # in `get_objects` method
        fields = [
            "id",
            "account_name",
            "created",
            "receive_date",
            "mail_box",
            "mail_id",
            "replay_to",
            "author_name",
            "author_mail",
            "subject",
            "body",
        ]

    def get_account_name(self, obj):
        return obj.mail_settings.smtp_username


class MailSettingsSerializer(AbstractSerializer):
    class Meta:
        model = MailSettings
        fields = [
            "id",
        ]


class MailSettingsLinkedSerializer(AbstractSerializer):
    class Meta:
        model = MailSettings
        fields = [
            "mail_folders",
            "smtp_server",
            "smtp_port",
            "smtp_username",
            "smtp_password",
            "imap_ssl",
            "imap_server",
            "imap_port",
            "imap_username",
            "imap_password",
        ]
        extra_kwargs = {
            "mail_folders": {"required": False},
        }
