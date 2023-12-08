import json
from typing import Any

from seo_parser.core.lib import SeoSite


class SimilarWeb(SeoSite):
    name = "Similarweb"
    url = "https://www.similarweb.com/ru/website/"
    validate_element = '//script[contains(text(),"window.__APP_DATA__")]'
    single_json_var = "window.__APP_DATA__"
    multi_json_var = False
    captcha = "Pardon Our Interruption..."
    parse_method = "browser"
    serialize_data: dict[Any, Any] = {"db_table_name": "similarweb"}

    def serialize(self) -> dict:
        if isinstance(self.value, dict):
            self.serialize_data["values"] = {}

            if not self.value.get("layout", {}):
                raise ValueError("SEO DATA NOT FOUND!")

            data: dict = self.value.get("layout", {}).get("data", {})

            sources = data.get("trafficSources", {})
            self.serialize_data["values"]["sources"] = {
                "direct": sources.get("directVisitsShare"),
                "referral": sources.get("referralVisitsShare"),
                "organic": sources.get("organicSearchVisitsShare"),
                "paid": sources.get("paidSearchVisitsShare"),
                "social": sources.get("socialNetworksVisitsShare"),
                "mail": sources.get("mailVisitsShare"),
                "ads": sources.get("adsVisitsShare"),
            }

            overview = data.get("overview", {})
            self.serialize_data["values"]["ranking"] = {
                "rank": overview.get("globalRank"),
                "country": overview.get("countryAlpha2Code"),
                "visits": overview.get("visitsTotalCount"),
                "bounce_rate": overview.get("bounceRate"),
                "page_per_visit": overview.get("pagesPerVisit"),
                "visit_time": overview.get("visitsAvgDurationFormatted"),
                "category": overview.get("companyCategoryId"),
            }

            interests = data.get("interests", {})
            self.serialize_data["values"]["interests"] = interests.get(
                "topInterestedTopics"
            )
            self.serialize_data["values"]["value"] = self.serialize_data[
                "values"
            ]["ranking"].get("rank", 0)

        return self.serialize_data

    def get_value(self) -> dict:
        page_content = self.page.locator(
            f"xpath={self.validate_element}"
        ).text_content()

        if page_content:
            value = self.page.evaluate("window.__APP_DATA__")
            if not value:
                value = page_content.split("\n")[1].replace(
                    "          window.__APP_DATA__ = ", ""
                )
            return json.loads(value) if isinstance(value, str) else value
        return {}
