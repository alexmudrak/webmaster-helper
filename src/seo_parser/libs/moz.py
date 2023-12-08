from seo_parser.core.lib import SeoSite


class Moz(SeoSite):
    name = "Moz"
    url = "https://moz.com/domain-analysis?site="
    validate_element = (
        '//div[contains(@class, "align-items-center")]/div[1]/h1'
    )
    single_json_var = False
    __xp = '//div[contains(@class, "align-items-center")]/div[{}]/h1'
    multi_json_var = {
        "da": __xp.format(1),
        "links": __xp.format(2),
        "keys_rank": __xp.format(3),
        "spam_score": __xp.format(4),
    }
    serialize_data = {"db_table_name": "moz"}
    captcha = "Pardon Our Interruption..."
    parse_method = "browser"

    def serialize(self) -> dict:
        if self.value:
            self.serialize_data["values"] = self.value
            if isinstance(self.serialize_data["values"], dict):
                self.serialize_data["values"]["value"] = self.serialize_data[
                    "values"
                ].get("da", 0)
        return self.serialize_data
