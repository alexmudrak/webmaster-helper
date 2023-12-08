from typing import Any

from seo_parser.core.lib import SeoSite


class YandexX(SeoSite):
    name = "Яндекс X"
    url = "https://webmaster.yandex.ru/siteinfo/?site="
    validate_element = '//script[contains(text(),"bh.lib.data")]'
    single_json_var = "bh.lib.data"
    multi_json_var = False
    captcha = "Ой"
    parse_method = "browser"
    serialize_data: dict[Any, Any] = {"db_table_name": "yandex_x"}

    def serialize(self) -> dict:
        if isinstance(self.value, dict):
            self.serialize_data["values"] = {}

            quality = self.value.get("quality", {})
            self.serialize_data["values"]["quality"] = quality.get(
                "achievements", [{}]
            )[0].get("sqi")

            rating = self.value.get("siteRating", {})
            self.serialize_data["values"]["rank"] = {
                "positive": rating.get("positiveCount", None),
                "negative": rating.get("negativeCount", None),
                "total": rating.get("totalCount", None),
            }
            self.serialize_data["values"]["value"] = self.serialize_data[
                "values"
            ]["quality"]

        return self.serialize_data
