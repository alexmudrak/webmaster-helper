from api.abstract.viewsets import AbstractViewSet
from api.auth.permissions import UserPermission
from api.webmaster.models import Payment
from api.webmaster.serializers import PaymentSerializer


class PaymentViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = PaymentSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializers):
        serializers.save(owner=self.request.user)

    def get_queryset(self):
        return Payment.objects.filter(owner=self.request.user.id)

    def get_object(self):
        obj = Payment.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
