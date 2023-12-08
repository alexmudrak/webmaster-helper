from typing import Any

from seo_parser.core.lib import SeoSite


class WebArchive(SeoSite):
    name = "Web archive"
    url = "http://web.archive.org/__wb/sparkline?output=json&url={}&collection=web"
    validate_element = ""
    single_json_var = ""
    multi_json_var = False
    captcha = "Captcha"
    parse_method = "request"
    serialize_data: dict[Any, Any] = {"db_table_name": "web_archive"}

    def serialize(self) -> dict:
        if isinstance(self.value, dict):
            oldest = self.value.get("first_ts")
            newest = self.value.get("last_ts")
            total = sum([sum(i) for i in self.value.get("years", {}).values()])

            self.serialize_data["values"] = {
                "oldest": oldest,
                "newest": newest,
                "total": total,
            }

            self.serialize_data["values"]["value"] = self.serialize_data[
                "values"
            ].get("total", 0)
        return self.serialize_data

    def parse_data_request(self, url: str) -> "SeoSite":
        if self.request_client:
            self.page = self.request_client.get_client
            response = self.page.get(
                self.url.format(url),
                headers={"Referer": "http://web.archive.org/web/*/" + url},
            )
            self.value = (
                response.json() if response.status_code == 200 else None
            )
        return self
