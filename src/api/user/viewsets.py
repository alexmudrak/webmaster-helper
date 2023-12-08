from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.auth.permissions import UserPermission
from api.mail_box.serializers import MailSettingsLinkedSerializer
from api.user.models import User
from api.user.serializers import UserSerializer
from mail.models import MailSettings


class UserViewSet(AbstractViewSet):
    http_method_names = ("patch", "get")
    permission_classes = (
        UserPermission,
        IsAuthenticated,
    )
    serializer_class = UserSerializer

    def get_queryset(self):
        # TODO: Need to delete `/api/user/` endpoint and response
        # only current user information
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = self.request.user

        if "mail_settings" in request.data:
            mail_settings_instance = user.mail_settings.filter(
                project=None
            ).first()

            mail_settings_data = request.data["mail_settings"]

            if mail_settings_data:
                if mail_settings_instance:
                    mail_settings_serializer = MailSettingsLinkedSerializer(
                        mail_settings_instance,
                        data=mail_settings_data,
                        partial=True,
                    )
                else:
                    mail_settings_serializer = MailSettingsLinkedSerializer(
                        data=mail_settings_data, partial=True
                    )

                mail_settings_serializer.is_valid(raise_exception=True)
                mail_settings_serializer.save(owner=user)
            else:
                if isinstance(mail_settings_instance, MailSettings):
                    mail_settings_instance.delete()

        return Response(serializer.data)
