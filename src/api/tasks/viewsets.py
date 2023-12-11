from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.tasks.seo_parse_task import get_seo_metrics
from api.url.models import Url


class TasksViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["GET"], url_path="get-all-seo-data")
    def run_collect_all_seo_data(self, request):
        urls = Url.objects.filter(
            websites__isnull=False,
            seo_check_date__lt=timezone.now() - timezone.timedelta(days=1),
        )

        for obj in urls:
            obj.seo_check_status = "PENDING"
            obj.save()
            get_seo_metrics.delay(obj.id)

        return Response({"task": "get-all-seo-data", "count": len(urls)})

    @action(detail=False, methods=["GET"], url_path="get-new-mails")
    def run_collect_new_mails(self, request):
        return Response({"task": "get-all-mails"})

    @action(detail=False, methods=["GET"], url_path="check-all-links")
    def run_check_all_links(self, request):
        return Response({"task": "check-all-links"})
