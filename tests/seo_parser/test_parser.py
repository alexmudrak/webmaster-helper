from unittest.mock import MagicMock, patch

import pytest

from api.url.models import Url
from seo_parser.models import SeoData
from seo_parser.parser import start_parser


@pytest.mark.django_db
@patch("seo_parser.parser.BrowserClient")
@patch("seo_parser.parser.RequestClient")
@patch("seo_parser.parser.seo_sites")
def test_start_parser(
    mock_seo_sites, mock_request_client, mock_browser_client
):
    url_obj = Url.objects.create(
        url="http://example.com", seo_check_status="DONE"
    )

    mock_obj = MagicMock()
    mock_obj.return_value.parse_data.return_value = {
        "db_table_name": "test_table",
        "values": {"value": "value_1"},
    }

    mock_seo_sites.__iter__.return_value = [mock_obj]

    start_parser(url_obj)

    seo_data = SeoData.objects.get(url=url_obj)
    assert seo_data.data == {"value": "value_1"}
