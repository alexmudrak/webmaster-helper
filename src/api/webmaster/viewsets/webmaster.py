from rest_framework import status
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.auth.permissions import UserPermission
from api.url.models import Url
from api.webmaster.models import Webmaster
from api.webmaster.models.contact import Contact
from api.webmaster.models.payment import Payment
from api.webmaster.models.website import Website
from api.webmaster.serializers import WebmasterSerializer
from utils.url_handlers import get_correct_url


class WebmasterViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = WebmasterSerializer
    permission_classes = (UserPermission,)

    def get_queryset(self):
        return Webmaster.objects.filter(owner=self.request.user.id)

    def get_object(self):
        obj = Webmaster.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        webmaster = serializer.save(owner=self.request.user)

        self._create_or_update_related_data(webmaster, request.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        self._create_or_update_related_data(instance, request.data)

        serializer.save()

        return Response(serializer.data)

    def _create_or_update_related_data(self, webmaster, data):
        contacts_data = data.get("contacts", [])
        websites_data = data.get("websites", [])
        payments_data = data.get("payments", [])

        for contact_data in contacts_data:
            if contact_data.get("contact"):
                if not contact_data.get("id"):
                    Contact.objects.create(
                        owner=self.request.user,
                        webmaster=webmaster,
                        type=contact_data["type"],
                        contact=contact_data["contact"],
                    )
                else:
                    contact = Contact.objects.get_object_by_public_id(
                        contact_data["id"]
                    )
                    contact.type = contact_data["type"]
                    contact.contact = contact_data["contact"]
                    contact.save()

        for website_data in websites_data:
            if website_data["site"]["url"]:
                normalized_url = get_correct_url(website_data["site"]["url"])
                website_data["url"], _ = Url.objects.get_or_create(
                    url=normalized_url
                )

                if not website_data.get("id"):
                    website = Website.objects.filter(
                        url__url=normalized_url, owner=self.request.user
                    ).first()
                    if not website:
                        website = Website.objects.create(
                            owner=self.request.user,
                            url=website_data["url"],
                        )

                    website.webmaster.add(webmaster)
                else:
                    website = Website.objects.get_object_by_public_id(
                        website_data.get("id")
                    )
                    if website_data["url"]:
                        website.url = website_data["url"]
                        website.save()

        for payment_data in payments_data:
            if payment_data["details"]:
                if not payment_data.get("id"):
                    Payment.objects.create(
                        owner=self.request.user,
                        webmaster=webmaster,
                        type=payment_data["type"],
                        details=payment_data["details"],
                    )
                else:
                    payment = Payment.objects.get_object_by_public_id(
                        payment_data["id"]
                    )
                    payment.type = payment_data["type"]
                    payment.details = payment_data["details"]
                    payment.save()
