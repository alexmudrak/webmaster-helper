from rest_framework.permissions import AllowAny

from api.abstract.viewsets import AbstractViewSet
from api.project.models import Project
from api.webmaster.models.publish_page import PublishPage
from api.webmaster.serializers.publish_page import PublishPageSerializer


class PublishPageViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = PublishPageSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        projects = Project.objects.filter(owner=self.request.user)
        publish_page = PublishPage.objects.filter(project__in=projects)
        return publish_page

    def get_object(self):
        obj = PublishPage.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
