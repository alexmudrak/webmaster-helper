from rest_framework import status
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.auth.permissions import UserPermission
from api.webmaster.models import Contact, Webmaster
from api.webmaster.serializers import (
    ContactRequestSerializer,
    ContactSerializer,
)


class ContactViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = ContactSerializer
    permission_classes = (UserPermission,)

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user.id)

    def get_object(self):
        obj = Contact.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializers):
        serializers.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        patch_serializer = ContactRequestSerializer(data=request.data)

        if patch_serializer.is_valid():
            webmaster_data = patch_serializer.validated_data.get(
                "webmaster", {}
            )
            webmaster_id = webmaster_data.get("id")

            try:
                webmaster = Webmaster.objects.get(public_id=webmaster_id)
            except Webmaster.DoesNotExist:
                return Response(
                    {"webmaster_id": "Invalid webmaster UUID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for attr, value in patch_serializer.validated_data.items():
                if attr != "webmaster":
                    setattr(instance, attr, value)

            instance.webmaster = webmaster
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(
                patch_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        create_serializer = ContactRequestSerializer(data=request.data)

        if create_serializer.is_valid():
            webmaster_data = create_serializer.validated_data.get(
                "webmaster", {}
            )
            webmaster_id = webmaster_data.get("id")
            type = create_serializer.validated_data.get("type")
            contact = create_serializer.validated_data.get("contact")
            owner_id = self.request.user.id

            try:
                webmaster = Webmaster.objects.get(public_id=webmaster_id)
            except Webmaster.DoesNotExist:
                return Response(
                    {"webmaster_id": "Invalid webmaster UUID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            contact = Contact(
                webmaster=webmaster,
                type=type,
                contact=contact,
                owner_id=owner_id,
            )
            contact.save()

            serializer = self.get_serializer(contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                create_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
