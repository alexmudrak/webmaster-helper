import pytest

from seo_parser.libs import YandexX
from tests.fixtures.seo_parser import mock_browser_client, mock_request_client

_ = mock_browser_client
_ = mock_request_client


class TestSeoParser:
    @pytest.fixture
    def seo_site_browser(self, mock_browser_client):
        seo_site = YandexX(browser_client=mock_browser_client())
        return seo_site

    def test_serialize_with_value(self, seo_site_browser):
        """
        Scenario: Test serialization of Yandex X instance with a specified
        value.
        When setting a value and serialize_data for a Yandex X instance.
        Then call the serialize method. Assert that the serialized result
        matches the expected structure.
        """
        # Arrange
        seo_site_browser.value = {"layout": {"mock_key": "mock_value"}}
        seo_site_browser.serialize_data = {"key": "data"}
        # Act
        result = seo_site_browser.serialize()
        # Assert
        expected_result = {
            "key": "data",
            "values": {
                "quality": None,
                "rank": {"negative": None, "positive": None, "total": None},
                "value": None,
            },
        }
        assert result == expected_result
