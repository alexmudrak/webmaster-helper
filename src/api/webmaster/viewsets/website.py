from datetime import datetime, timezone
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status

from api.abstract.viewsets import AbstractViewSet
from api.project.models import Project
from api.tasks.link_check_task import get_link_check
from api.tasks.seo_parse_task import get_seo_metrics
from api.url.models import Url
from api.webmaster.models.publish_page import PublishPage
from api.webmaster.models.webmaster import Webmaster
from api.webmaster.models.website import Website
from api.webmaster.serializers.website import WebsiteSerializer
from core.exceptions import DuplicateError
from utils.logger_handler import get_logger
from utils.url_handlers import get_correct_domain, get_correct_url

logger = get_logger(__name__)


# TODO: Add typing
class WebsiteViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "patch", "delete")
    serializer_class = WebsiteSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Website.objects.filter(owner=self.request.user)

    def get_object(self):
        obj = Website.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, *args, **kwargs):
        website = self.get_object()
        data = self.request.data
        owner = self.request.user
        url_data = data.get("site", {})
        information = data.get("information", "")
        publish_cost_data = data.get("publish_cost", 0.00)
        projects_data = data.get("projects")
        webmasters_list = data.get("webmasters")

        self.validate_url_data(url_data)

        with transaction.atomic():
            url = self.get_or_create_url(url_data.get("url"))
            website.webmaster.clear()
            self.update_webmasters(website, webmasters_list, owner)

            obj_data = {
                "owner": owner,
                "url": url,
                "publish_cost": Decimal(publish_cost_data),
                "information": information,
            }
            logger.debug(f"Object for update Website: {obj_data}")
            self.update_website(website, obj_data)
            if projects_data:
                self.create_or_update_publish_pages(website, projects_data)
        return Response(
            {
                "message": "Website updated successfully",
                "website_id": website.public_id,
            },
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):
        data = self.request.data
        owner = self.request.user
        url_data = data.get("site")
        information = data.get("information", "")
        publish_cost_data = data.get("publish_cost", 0.00)
        projects_data = data.get("projects")
        webmasters_list = data.get("webmasters")

        self.validate_url_data(url_data)

        with transaction.atomic():
            url = self.get_or_create_url(url_data["url"])
            website = serializer.save(
                url=url,
                owner=owner,
                publish_cost=publish_cost_data,
                information=information,
            )
            self.update_webmasters(website, webmasters_list, owner)
            if projects_data:
                self.create_or_update_publish_pages(website, projects_data)
        return Response(
            {
                "message": "Website created successfully",
                "website_id": website.public_id,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="run-seo-task")
    def seo_task(self, request, pk=None):
        try:
            obj = Url.objects.get_object_by_public_id(pk)
            obj.seo_check_status = "PENDING"
            obj.save()

            self.check_object_permissions(request, obj)

            task = get_seo_metrics.delay(obj.id)

            return Response(
                {
                    "url": obj.url,
                    "status": obj.seo_check_status,
                    "task_id": task.id,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Http404:
            return Response(
                {"detail": f"URL {pk} - Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=["post"], url_path="run-check-links")
    def check_links_task(self, request, pk=None):
        website = Website.objects.get_object_by_public_id(pk)
        publish_pages = PublishPage.objects.filter(website=website)

        response_status = []
        for obj in publish_pages:
            try:
                obj.check_status = "PENDING"
                obj.save()

                task = get_link_check.delay(obj.id)

                response_status.append(
                    {
                        "url": obj.url,
                        "status": obj.check_status,
                        "task_id": task.id,
                    }
                )
            except Http404:
                response_status.append(
                    {
                        "url": obj.publish_page,
                        "status": "Not found",
                    }
                )
        return Response(
            {
                "results": response_status,
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def validate_url_data(self, url_data):
        if not url_data or not url_data.get("url"):
            raise ValidationError({"detail": "Empty or missing URL value."})

    def get_or_create_url(self, url):
        try:
            return Url.objects.get_or_create(url=get_correct_domain(url))[0]
        except ValueError:
            raise ValidationError({"detail": "Invalid website URL value."})

    def create_or_update_publish_pages(self, website, projects_data):
        for project in projects_data:
            project_instance = Project.objects.get(public_id=project["id"])
            self.create_or_update_publish_page(
                website, project_instance, project.get("publish_pages")
            )

    def create_or_update_publish_page(
        self, website: Website, project: Project, publish_pages: list
    ):
        for publish_page in publish_pages:
            publish_page_id = publish_page.get("id")
            publish_page_date_str = publish_page.get(
                "publish_date", datetime.now(timezone.utc)
            )
            publish_page_date = datetime.now(timezone.utc)

            if not isinstance(publish_page_date_str, datetime):
                try:
                    publish_page_date = datetime.strptime(
                        publish_page_date_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).replace(tzinfo=timezone.utc)
                except ValueError:
                    try:
                        publish_page_date = datetime.strptime(
                            publish_page_date_str, "%Y-%m-%d"
                        ).replace(tzinfo=timezone.utc)
                    except ValueError:
                        logger.error(
                            "Problem with converting datetime: "
                            f"{publish_page_date_str} to `%Y-%m-%d`"
                        )

            publish_page_url = get_correct_url(publish_page.get("url", ""))

            logger.info(f"Create Publish page url: {publish_page_url}")

            if publish_page_id is not None:
                result, _ = PublishPage.objects.get_or_create(
                    public_id=publish_page_id
                )
                new_url = publish_page_url
                if new_url and result.url != new_url:
                    result.url = new_url
                result.publish_date = publish_page_date
                result.save()
            else:
                result, _ = PublishPage.objects.get_or_create(
                    project=project,
                    url=publish_page_url,
                )
                result.website = website
                result.publish_date = publish_page_date
                result.save()

    def update_webmasters(self, website, webmasters_list, owner):
        if webmasters_list:
            for webmaster_data in webmasters_list:
                webmaster, _ = Webmaster.objects.get_or_create(
                    owner=owner, name=webmaster_data.get("name")
                )
                website.webmaster.add(webmaster)

    def update_website(self, website, obj_data):
        new_url = obj_data["url"]

        if Website.objects.filter(url=new_url).exclude(pk=website.pk).exists():
            raise DuplicateError(
                {
                    "detail": (
                        "This URL is already associated with another website."
                    )
                }
            )

        website.url = new_url
        serializer = self.get_serializer(website, data=obj_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @staticmethod
    def handle_integrity_error():
        try:
            with transaction.atomic():
                yield
        except IntegrityError:
            raise DuplicateError({"detail": "This website already exists."})
