from rest_framework import serializers

from api.abstract.serializers import AbstractSerializer
from api.url.serializers import UrlSerializer
from api.webmaster.models import Contact, Webmaster
from api.webmaster.models.payment import Payment
from api.webmaster.models.website import Website


class ContactSerializer(AbstractSerializer):
    latest_contact = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "id",
            "type",
            "contact",
            "latest_contact",
        ]

    def get_latest_contact(self, obj):
        from api.webmaster.serializers.contact_history import (
            ContactHistorySerializer,
        )

        latest_contact_history = obj.contact_history.last()

        if latest_contact_history:
            data = ContactHistorySerializer(
                instance=latest_contact_history
            ).data
            return data.get("created", None)
        else:
            return None


class WebmasterIncludeSerializer(AbstractSerializer):
    class Meta:
        model = Webmaster
        fields = [
            "id",
            "name",
        ]


class WebsitesWebmasterSerializer(AbstractSerializer):
    site = UrlSerializer(source="url", required=False)

    class Meta:
        model = Website
        fields = [
            "id",
            "site",
        ]


class PaymentWebmasterSerializer(AbstractSerializer):
    total_spend = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "total_spend",
            "type",
            "details",
        ]

    def get_total_spend(self, obj):
        payment_histories = obj.payment_history.all()
        total_spend = sum(
            history.price
            for history in payment_histories
            if history.price is not None
        )
        return total_spend


class WebmasterLessSerializer(AbstractSerializer):
    class Meta:
        model = Webmaster
        fields = [
            "id",
            "name",
        ]


class WebmasterSerializer(AbstractSerializer):
    websites = WebsitesWebmasterSerializer(
        many=True, required=False, read_only=True
    )
    payments = PaymentWebmasterSerializer(
        many=True, required=False, source="payment", read_only=True
    )
    contacts = ContactSerializer(
        many=True, required=False, source="contact", read_only=True
    )

    class Meta:
        model = Webmaster
        fields = [
            "id",
            "name",
            "contacts",
            "websites",
            "payments",
        ]
