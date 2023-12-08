from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.auth.permissions import UserPermission
from api.project.models import Project
from api.webmaster.models import PaymentHistory
from api.webmaster.models.payment import Payment
from api.webmaster.models.website import Website
from api.webmaster.serializers import PaymentHistorySerializer


class PaymentHistoryViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = PaymentHistorySerializer
    permission_classes = (UserPermission,)

    RELATED_OBJECTS = {
        "payment": Payment,
        "website": Website,
        "project": Project,
    }

    def get_queryset(self):
        return PaymentHistory.objects.filter(owner=self.request.user.id)

    def get_object(self):
        obj = PaymentHistory.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer: PaymentHistorySerializer):
        self._process_create_or_partial_update(serializer)

    def partial_update(self, *args, **kwargs):
        return self._process_create_or_partial_update(
            self.get_serializer(), is_partial_update=True
        )

    def _validate_data_format(self, data):
        if not isinstance(data, dict):
            raise ValueError("Invalid data format")

    def _get_related_entities(self, data):
        return {
            key: self.RELATED_OBJECTS[key].objects.get_object_by_public_id(
                value.get("id")
            )
            for key, value in data.items()
            if key in self.RELATED_OBJECTS.keys()
        }

    def _handle_invalid_ids(self, related_entities):
        if not all(related_entities.values()):
            return Response(
                {
                    "detail": (
                        "Invalid public ID for one or " "more related objects"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _update_serializer_data(self, serializer, related_entities):
        serializer.validated_data.update(related_entities)

    def _extract_price_from_data(self, data):
        return Decimal(data.get("price", "0"))

    def _process_create_or_partial_update(
        self, serializer, is_partial_update=False
    ):
        data = self.request.data
        self._validate_data_format(data)

        related_entities = self._get_related_entities(data)

        if self._handle_invalid_ids(related_entities):
            return

        instance = self.get_object() if is_partial_update else None
        serializer = self.get_serializer(
            instance, data=data, partial=is_partial_update
        )
        serializer.is_valid(raise_exception=True)

        self._update_serializer_data(serializer, related_entities)

        serializer.save(
            owner=self.request.user, price=self._extract_price_from_data(data)
        )

        return Response(serializer.data)
