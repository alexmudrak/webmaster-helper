from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.tasks.link_check_task import get_link_check
from api.tasks.mail_task import get_mails
from api.tasks.seo_parse_task import get_seo_metrics
from api.url.models import Url
from api.webmaster.models.publish_page import PublishPage
from mail.models import MailSettings


class TasksViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["GET"], url_path="get-all-seo-data")
    def run_collect_all_seo_data(self, request):
        """
        Collect SEO data for all URLs, ensuring that each one is linked to the
        website and that the last SEO status check was performed no more than
        1 day ago.
        """
        # TODO: Add permission check.
        urls = Url.objects.filter(
            websites__isnull=False,
            seo_check_date__lt=timezone.now() - timezone.timedelta(days=1),
        )

        for obj in urls:
            obj.seo_check_status = "PENDING"
            obj.save()
            get_seo_metrics.delay(obj.id)

        return Response(
            {
                "task": "get-all-seo-data",
                "count": len(urls),
            }
        )

    @action(detail=False, methods=["GET"], url_path="get-new-mails")
    def run_collect_new_mails(self, request):
        """
        Collect mails for all MailSettings that the last status check was
        performed no more than 1 day ago.
        """
        # TODO: Add permission check.
        mail_settings = MailSettings.objects.filter(
            check_date__lt=timezone.now() - timezone.timedelta(days=1),
        )

        for obj in mail_settings:
            obj.check_status = "PENDING"
            obj.save()
            get_mails.delay(obj.id)

        return Response(
            {
                "task": "get-all-mails",
                "count": len(mail_settings),
            }
        )

    @action(detail=False, methods=["GET"], url_path="check-all-links")
    def run_check_all_links(self, request):
        """
        Check all published pages for the provided links on webmaster websites
        that the last status check was performed no more than 1 day ago and
        collect all anchors and links.
        """
        # TODO: Add permission check.
        pages = PublishPage.objects.filter(
            check_date__lt=timezone.now() - timezone.timedelta(days=1),
        )

        for obj in pages:
            obj.check_status = "PENDING"
            obj.save()
            get_link_check.delay(obj.id)

        return Response(
            {
                "task": "check-all-links",
                "count": len(pages),
            }
        )
