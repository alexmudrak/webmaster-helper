from unittest.mock import create_autospec

import pytest
from playwright.sync_api import Error, Page

from seo_parser.libs import SimilarWeb
from tests.fixtures.seo_parser import mock_browser_client, mock_request_client

_ = mock_browser_client
_ = mock_request_client


class TestSeoParser:
    @pytest.fixture
    def seo_site_browser(self, mock_browser_client):
        seo_site = SimilarWeb(browser_client=mock_browser_client())
        return seo_site

    def test_serialize_with_value(self, seo_site_browser):
        """
        Scenario: Test serialization of SimilarWeb instance with a specified
        value.
        When setting a value and serialize_data for a SimilarWeb instance.
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
                "sources": {
                    "direct": None,
                    "referral": None,
                    "organic": None,
                    "paid": None,
                    "social": None,
                    "mail": None,
                    "ads": None,
                },
                "ranking": {
                    "rank": None,
                    "country": None,
                    "visits": None,
                    "bounce_rate": None,
                    "page_per_visit": None,
                    "visit_time": None,
                    "category": None,
                },
                "interests": None,
                "value": None,
            },
        }
        assert result == expected_result

    def test_parse_goto_browser_error(self, seo_site_browser):
        """
        Scenario: Test handling browser error during the parse_data_browser
        method.
        When encountering a browser error during the parse_data_browser method.
        Then ensure the result value is the SeoSite's current value. Assert
        that the page's goto method is called with the expected URL. Assert
        that the page's locator method is called three times. Assert that the
        locator's is_enabled method is called once.
        """
        # Arrange
        mock_page = create_autospec(Page)
        mock_page.goto.side_effect = Error("Test error")
        seo_site_browser.get_client = mock_page
        # Act
        result = seo_site_browser.parse_data_browser("/example-url")
        # Assert
        assert result.value == seo_site_browser.get_value()
        seo_site_browser.page.goto.assert_called_once_with(
            seo_site_browser.url + "/example-url"
        )
        assert seo_site_browser.page.locator.call_count == 3
        seo_site_browser.page.locator.return_value.is_enabled.assert_called_once()
