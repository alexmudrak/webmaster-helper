from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status

from api.abstract.viewsets import AbstractViewSet
from api.mail_box.serializers import MailBoxSerializer
from api.tasks.mail_task import get_mails
from mail.models import Mail, MailSettings


class MailBoxViewSet(AbstractViewSet):
    http_method_names = ("get", "post")
    serializer_class = MailBoxSerializer
    # TODO: Change permission to UserPermission
    # permission_classes = (UserPermission,)
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def get_queryset(self):
        owner = self.request.user
        mail_settings = MailSettings.objects.filter(owner=owner)

        mails = Mail.objects.filter(mail_settings__in=mail_settings).order_by(
            "-receive_date"
        )
        return mails

    def get_object(self):
        obj = Mail.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)

        return obj

    @action(detail=False, methods=["post"], url_path="run-get-mails")
    def get_mails_task(self, request):
        owner = request.user
        mails_settings = MailSettings.objects.filter(owner=owner)

        mail_boxes = []
        for mail_settings in mails_settings:
            mail_settings.check_status = "PENDING"
            mail_settings.save()
            mail_boxes.append(mail_settings.smtp_username)
            task = get_mails.delay(mail_settings.id)
        return Response(
            {
                "mail_box": mail_boxes,
                "task_id": task.id,
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=["get"], url_path="get-mailbox-status")
    def get_mailbox_status(self, request):
        owner = request.user
        mails_settings = MailSettings.objects.filter(owner=owner)

        mail_boxes = []
        for mail_settings in mails_settings:
            data = {
                "mailbox": mail_settings.smtp_username,
                "status": mail_settings.check_status,
            }
            mail_boxes.append(data)
        return Response(
            mail_boxes,
            status=status.HTTP_202_ACCEPTED,
        )
