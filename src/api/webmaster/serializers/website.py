from rest_framework import serializers

from api.abstract.serializers import AbstractSerializer
from api.project.models import Project
from api.url.serializers import UrlSerializer
from api.webmaster.models import Website
from api.webmaster.serializers.webmaster import WebmasterIncludeSerializer
from seo_parser.serializers import SeoDataSerializer


class WebsiteLessSerializer(AbstractSerializer):
    site = UrlSerializer(source="url", read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = [
            "id",
            "site",
            "name",
        ]

    def get_name(self, obj):
        return obj.url.url if obj.url else None


class WebsiteSerializer(AbstractSerializer):
    site = UrlSerializer(source="url", read_only=True)
    seo_data = serializers.SerializerMethodField(read_only=True)
    publish_efficiency = serializers.SerializerMethodField(read_only=True)
    projects = serializers.SerializerMethodField(read_only=True)
    webmasters = WebmasterIncludeSerializer(
        source="webmaster",
        many=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = Website
        fields = [
            "id",
            "site",
            "information",
            "publish_cost",
            "publish_efficiency",
            "seo_data",
            "webmasters",
            "projects",
        ]

    def get_publish_efficiency(self, obj) -> float:
        def get_normalized_value(data, key):
            value = (
                data.get(key, {}).get("data", {}).get("value")
                if data and data.get(key) and data.get(key).get("data")
                else 0
            )
            return int(value) if value else 0

        def calculate_metric(value, divisor):
            value = value or 0
            return value / price / divisor if price > 0 else value / divisor

        seo_data = self.get_seo_data(obj)
        price = float(obj.publish_cost) if obj.publish_cost else 0

        yandex_x_data = get_normalized_value(seo_data, "yandex_x")
        similarweb_data = get_normalized_value(seo_data, "similarweb")
        moz_data = get_normalized_value(seo_data, "moz")
        web_archive_data = get_normalized_value(seo_data, "web_archive")

        site_source_traffic = (
            seo_data.get("similarweb", {})
            .get("data", {})
            .get("sources", {})
            .get("organic", 0)
            if seo_data.get("similarweb") and seo_data.get("data")
            else 0
        )

        calculate_yandex_x = calculate_metric(yandex_x_data, 10)
        calculate_similarweb = calculate_metric(
            (10_000_000 - similarweb_data) if similarweb_data else 0, 1_000_000
        )
        calculate_moz = calculate_metric(moz_data, 1)
        calculate_web_archive = calculate_metric(web_archive_data, 10)

        calculate_sum = (
            calculate_yandex_x
            + calculate_similarweb
            + calculate_moz
            + calculate_web_archive
        )

        return float(calculate_sum + calculate_sum * site_source_traffic)

    def get_seo_data(self, obj):
        yandex_x = (
            obj.url.seo_data.exclude(data__has_key="error")
            .filter(type="yandex_x")
            .last()
        )
        similarweb = (
            obj.url.seo_data.exclude(data__has_key="error")
            .filter(type="similarweb")
            .last()
        )
        moz = (
            obj.url.seo_data.exclude(data__has_key="error")
            .filter(type="moz")
            .last()
        )
        web_archive = (
            obj.url.seo_data.exclude(data__has_key="error")
            .filter(type="web_archive")
            .last()
        )

        data = {
            "yandex_x": SeoDataSerializer(instance=yandex_x).data,
            "similarweb": SeoDataSerializer(instance=similarweb).data,
            "moz": SeoDataSerializer(instance=moz).data,
            "web_archive": SeoDataSerializer(instance=web_archive).data,
        }
        data["created"] = obj.url.updated
        return data

    def get_projects(self, obj):
        user = obj.owner

        projects = Project.objects.filter(owner=user)

        project_data_dict = {
            project.public_id.hex: {
                "id": project.public_id.hex,
                "name": project.name,
                "publish_pages": [],
            }
            for project in projects
        }

        for publish_page_instance in obj.publish_page.all():
            project_instance = publish_page_instance.project
            url = publish_page_instance.url
            url_id = publish_page_instance.public_id.hex
            url_check_date = publish_page_instance.check_date
            url_check_status = publish_page_instance.check_status
            publish_date = publish_page_instance.publish_date

            project_id = project_instance.public_id.hex
            if project_id not in project_data_dict:
                project_data_dict[project_id] = {
                    "id": project_id,
                    "name": project_instance.name,
                    "publish_pages": [],
                }

            project_data_dict[project_id]["publish_pages"].append(
                {
                    "id": url_id,
                    "url": url or None,
                    "check_status": url_check_status or None,
                    "publish_date": publish_date or None,
                    "check_date": url_check_date or None,
                }
            )

            current_last_publish_check = project_data_dict[project_id].get(
                "last_publish_check", None
            )
            if (
                current_last_publish_check is None
                or url_check_date > current_last_publish_check
            ):
                project_data_dict[project_id][
                    "last_publish_check"
                ] = url_check_date

        project_data_list = list(project_data_dict.values())

        return project_data_list
