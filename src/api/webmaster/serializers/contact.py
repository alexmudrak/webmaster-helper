from rest_framework import serializers

from api.abstract.serializers import AbstractSerializer
from api.webmaster.models import Contact, ContactHistory
from api.webmaster.serializers.webmaster import WebmasterSerializer


class WebmasterRequestSerializer(serializers.Serializer):
    id = serializers.CharField()


class ContactRequestSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)
    webmaster = WebmasterRequestSerializer()


class ContactLessSerializer(AbstractSerializer):
    type = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)

    class Meta:
        model = Contact
        fields = [
            "id",
            "type",
            "contact",
        ]


class ContactSerializer(AbstractSerializer):
    webmaster = WebmasterSerializer()
    last_contact_date = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "id",
            "type",
            "contact",
            "webmaster",
            "last_contact_date",
            "created",
            "updated",
        ]

    def get_last_contact_date(self, obj):
        from api.webmaster.serializers.contact_history import (
            ContactHistorySerializer,
        )

        latest_history = ContactHistory.objects.filter(contact=obj).order_by(
            "-created"
        )

        if latest_history.exists():
            latest_contact_history = latest_history.first()

            result = ContactHistorySerializer(latest_contact_history).data
            return result.get("created")
        else:
            return None
