from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class TasksViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["GET"], url_path="get-all-seo-data")
    def run_collect_all_seo_data(self, request):
        return Response({"task": "get-all-seo-data"})

    @action(detail=False, methods=["GET"], url_path="get-new-mails")
    def run_collect_new_mails(self, request):
        return Response({"task": "get-all-mails"})

    @action(detail=False, methods=["GET"], url_path="check-all-links")
    def run_check_all_links(self, request):
        return Response({"task": "check-all-links"})
