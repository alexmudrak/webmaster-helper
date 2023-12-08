from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import status

from api.abstract.viewsets import AbstractViewSet
from api.auth.permissions import UserPermission
from api.project.models import Project
from api.tasks.mail_task import send_mails
from api.webmaster.models import Contact, ContactHistory, Webmaster, Website
from api.webmaster.serializers import ContactHistorySerializer
from mail.models import MailSettings
from utils.logger_handler import get_logger

logger = get_logger(__name__)


class ContactHistoryViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = ContactHistorySerializer
    permission_classes = (UserPermission,)

    def get_queryset(self):
        return ContactHistory.objects.filter(owner=self.request.user.id)

    def get_object(self):
        obj = ContactHistory.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        message = self.get_object()
        data = request.data

        project_id = data.get("project", {}).get("id")
        webmaster_id = data.get("webmaster", {}).get("id")
        website_id = data.get("website", {}).get("id")
        contact_id = data.get("contact", {}).get("id")

        project = get_object_or_404(Project, public_id=project_id)
        webmaster = get_object_or_404(Webmaster, public_id=webmaster_id)
        website = get_object_or_404(Website, public_id=website_id)
        contact = get_object_or_404(Contact, public_id=contact_id)

        serializer = self.get_serializer(message, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            project=project,
            webmaster=webmaster,
            website=website,
            contact=contact,
        )

        return Response(
            {
                "message": "Message updated successfully",
                "website_id": message.public_id,
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def create(self, _):
        owner = self.request.user
        data = self.request.data
        serializer = ContactHistorySerializer(data=data)
        serializer.is_valid(raise_exception=True)

        project_id = data.get("project", {}).get("id")
        webmaster_id = data.get("webmaster", {}).get("id")
        website_id = data.get("website", {}).get("id")
        contact_id = data.get("contact", {}).get("id")
        subject_data = data.get("subject", "")
        body_data = data.get("body", "")

        project = get_object_or_404(Project, public_id=project_id)
        webmaster = get_object_or_404(Webmaster, public_id=webmaster_id)
        website = get_object_or_404(Website, public_id=website_id)
        contact = get_object_or_404(Contact, public_id=contact_id)

        message = serializer.save(
            owner=owner,
            project=project,
            webmaster=webmaster,
            website=website,
            contact=contact,
            subject=subject_data,
            body=body_data,
        )

        task = None
        if contact.type.lower() == "email":
            task = self._send_mails_task(message, project)

        return Response(
            {
                "message": "Message created successfully",
                "message_id": message.public_id,
                "task": task.id if task else task,
            },
            status=status.HTTP_201_CREATED,
        )

    def _send_mails_task(self, message: ContactHistory, project: Project):
        owner = message.owner
        mail_setting = (
            MailSettings.objects.filter(project=message.project).first()
            or MailSettings.objects.filter(owner=owner, project=None).first()
        )

        if mail_setting:
            try:
                mail_data = {
                    "subject": message.subject,
                    "message": message.body,
                    "from_email": mail_setting.smtp_username,
                    "recipient": message.contact.contact,
                }

                task = send_mails.delay(
                    project.id,
                    mail_setting.id,
                    mail_data,
                )
                return task
            except Exception as e:
                # TODO: Add proper error handling
                # For now, just print the exception
                logger.error(f"Error sending mail: {e}")
            return False
