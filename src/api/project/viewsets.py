from rest_framework import status
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.auth.permissions import UserPermission
from api.mail_box.serializers import MailSettingsLinkedSerializer
from api.project.models import Project
from api.project.serializers import ProjectSerializer
from api.url.models import Url
from mail.models import MailSettings
from utils.url_handlers import get_correct_url


class ProjectViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = ProjectSerializer
    permission_classes = (UserPermission,)

    def handler_mail_settings(self, project, user, mail_settings):
        if mail_settings is not None:
            mail_settings_serializer = MailSettingsLinkedSerializer(
                data=mail_settings
            )
            mail_settings_serializer.is_valid(raise_exception=True)
            (
                mail_settings_instance,
                created,
            ) = MailSettings.objects.get_or_create(
                project=project,
                owner=user,
                defaults=mail_settings_serializer.validated_data,
            )
            if not created:
                for (
                    attr,
                    value,
                ) in mail_settings_serializer.validated_data.items():
                    setattr(mail_settings_instance, attr, value)

                mail_settings_instance.save()
        else:
            try:
                mail_settings_instance = MailSettings.objects.get(
                    project=project, owner=user
                )
                mail_settings_instance.delete()
            except MailSettings.DoesNotExist:
                pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data.get("url")
        name = serializer.validated_data.get("name")

        if not url:
            return Response(
                {"error": "url is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not name:
            return Response(
                {"error": "name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = self.request.user
        url = request.data.get("url", None)
        name = request.data.get("name", None)
        mail_settings = request.data.get("mail_settings", None)

        url_obj, _ = Url.objects.get_or_create(
            url=get_correct_url(url.get("url"))
        )

        obj_data = {
            "name": name,
            "owner": user,
        }
        serializer = self.get_serializer(data=obj_data)

        if serializer.is_valid():
            project = Project.objects.create(
                name=name, url=url_obj, owner=user
            )
            serializer_data = serializer.data
            serializer_data["id"] = project.public_id.hex
            serializer_data["url"] = project.url.url

            self.handler_mail_settings(project, user, mail_settings)

            return Response(serializer_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, *args, **kwargs):
        project = self.get_object()
        user = self.request.user
        url = request.data.get("url", None)
        name = request.data.get("name", None)
        mail_settings = request.data.get("mail_settings", None)

        url_obj, _ = Url.objects.get_or_create(
            url=get_correct_url(url.get("url"))
        )

        self.handler_mail_settings(project, user, mail_settings)

        obj_data = {
            "name": name,
            "owner": user,
        }

        project.url = url_obj

        serializer = self.get_serializer(project, data=obj_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Project updated successfully",
                "project_id": project.public_id,
            },
            status=status.HTTP_200_OK,
        )

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user.id)

    def get_object(self):
        obj = Project.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)

        return obj
