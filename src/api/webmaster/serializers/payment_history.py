from rest_framework import serializers

from api.abstract.serializers import AbstractSerializer
from api.webmaster.models import PaymentHistory


class PaymentHistorySerializer(AbstractSerializer):
    payment = serializers.SerializerMethodField()
    website = serializers.SerializerMethodField()
    webmaster = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = PaymentHistory
        fields = [
            "id",
            "price",
            "created",
            "website",
            "payment",
            "webmaster",
            "project",
        ]

    def get_project(self, obj):
        if hasattr(obj, "project"):
            project = {
                "id": obj.project.public_id.hex,
                "name": obj.project.name,
            }
            return project
        return None

    def get_payment(self, obj):
        if hasattr(obj, "payment"):
            payment = obj.payment
            data = {
                "id": payment.public_id.hex,
                "type": payment.type,
                "detail": payment.details,
            }
            return data if obj.website else None
        return None

    def get_website(self, obj):
        if hasattr(obj, "website"):
            url = obj.website.url
            data = {
                "id": obj.website.public_id.hex,
                "name": url.url,
            }
            return data if obj.website else None
        return None

    def get_webmaster(self, obj):
        if hasattr(obj, "payment"):
            webmaster = obj.payment.webmaster
            data = {
                "id": webmaster.public_id.hex,
                "name": webmaster.name,
            }
            return data if obj.payment else None
        return None
