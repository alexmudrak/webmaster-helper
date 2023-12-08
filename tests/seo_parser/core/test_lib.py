from itertools import cycle
from unittest.mock import MagicMock, call, create_autospec

import pytest
from playwright.sync_api import Error, Page

from seo_parser.core.lib import SeoSite
from tests.fixtures.seo_parser import mock_browser_client, mock_request_client

_ = mock_browser_client
_ = mock_request_client


class TestSeoParser:
    @pytest.fixture
    def seo_site_browser(self, mock_browser_client):
        seo_site = SeoSite(browser_client=mock_browser_client())
        seo_site.name = "Mock Single"
        seo_site.url = "https://example.com"
        seo_site.validate_element = "//some/xpath"
        seo_site.parse_method = "browser"
        seo_site.single_json_var = "mock"
        seo_site.serialize_data = {"db_mock": "mock"}
        seo_site.captcha = "Pardon Our Interruption..."
        return seo_site

    @pytest.fixture
    def seo_site_request(self, mock_request_client):
        seo_site = SeoSite(request_client=mock_request_client())
        seo_site.name = "Mock Single"
        seo_site.url = "https://example.com"
        seo_site.validate_element = ""
        seo_site.parse_method = "request"
        seo_site.single_json_var = False
        seo_site.serialize_data = {"db_mock": "mock"}
        seo_site.captcha = "Captcha"
        return seo_site

    def test_initialize_seo_site(self, mock_browser_client):
        """
        Scenario: Test the initialization of a SeoSite instance with a mock
        browser client.
        When creating a SeoSite instance with a mock browser client.
        Then ensure the SeoSite object is not None. And ensure the SeoSite
        object has a non-None browser client attribute.
        """
        # Arrange
        # Act
        seo_site = SeoSite(browser_client=mock_browser_client)
        # Assert
        assert seo_site is not None
        assert seo_site.browser_client is not None

    def test_serialize_with_value(self, seo_site_browser):
        """
        Scenario: Test the serialization of a SeoSite instance with a specified
        value.
        When setting a value and serialize_data for a SeoSite instance.
        Then call the serialize method. Assert that the serialized result
        matches the expected structure.
        """
        # Arrange
        seo_site_browser.value = {"key": "value"}
        seo_site_browser.serialize_data = {"key": "data"}
        # Act
        result = seo_site_browser.serialize()
        # Assert
        expected_result = {
            "key": "data",
            "values": {"value": {"key": "value"}},
        }
        assert result == expected_result

    def test_parse_goto_browser_error(self, seo_site_browser):
        """
        Scenario: Test handling browser error during the parse_data_browser
        method.
        When encountering a browser error during the parse_data_browser method.
        Then ensure the result value is the SeoSite's current value. Assert
        that the page's goto method is called with the expected URL. Assert
        that the page's locator method is called with the expected XPath.
        Assert that the locator's is_enabled method is called once.
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
        seo_site_browser.page.locator.assert_called_once_with(
            f"xpath={seo_site_browser.validate_element}"
        )
        seo_site_browser.page.locator.return_value.is_enabled.assert_called_once()

    def test_parse_single_json_var_data_browser_success(
        self, seo_site_browser
    ):
        """
        Scenario: Test successful parsing of single JSON variable data using
        the browser method.
        When successfully parsing data with a single JSON variable using the
        browser method.
        Then ensure the result value matches the SeoSite's current value.
        Assert that the page's goto method is called with the expected URL.
        Assert that the page's locator method is called with the expected
        XPath.
        Assert that the locator's is_enabled method is called once.
        """
        # Arrange
        mock_page = create_autospec(Page)
        mock_page.goto.return_value = MagicMock()
        mock_page.evaluate.return_value = "test mock"
        seo_site_browser.get_client = mock_page
        # Act
        result = seo_site_browser.parse_data_browser("/example-url")
        # Assert
        assert result.value == seo_site_browser.get_value()
        seo_site_browser.page.goto.assert_called_once_with(
            seo_site_browser.url + "/example-url"
        )
        seo_site_browser.page.locator.assert_called_once_with(
            f"xpath={seo_site_browser.validate_element}"
        )
        seo_site_browser.page.locator.return_value.is_enabled.assert_called_once()

    def test_parse_multi_json_var_data_browser_success(self, seo_site_browser):
        """
        Scenario: Test successful parsing of multi JSON variable data using
        the browser method.
        When successfully parsing data with multiple JSON variables using the
        browser method.
        Then ensure the result value matches the SeoSite's current value.
        Assert that the page's goto method is called with the expected URL.
        Assert that the page's locator method is called with the expected
        XPaths in any order.
        Assert that each locator's is_enabled method is called once.
        """
        # Arrange
        mock_page = create_autospec(Page)
        mock_page.goto.return_value = MagicMock()
        mock_page.locator.return_value.inner_text.side_effect = cycle(
            [
                "value_1",
                "value_2",
                "value_3",
                "value_4",
            ]
        )
        seo_site_browser.browser_client.get_client = mock_page
        seo_site_browser.single_json_var = False
        seo_site_browser.multi_json_var = {
            "mock_1": "mock_xpath_1",
            "mock_2": "mock_xpath_2",
            "mock_3": "mock_xpath_3",
            "mock_4": "mock_xpath_4",
        }
        # Act
        result = seo_site_browser.parse_data_browser("/example-url")
        # Assert
        assert result.value == seo_site_browser.get_value()
        seo_site_browser.page.goto.assert_called_once_with(
            seo_site_browser.url + "/example-url"
        )
        seo_site_browser.page.locator.assert_has_calls(
            [
                call("mock_xpath_1"),
                call("mock_xpath_2"),
                call("mock_xpath_3"),
                call("mock_xpath_4"),
            ],
            any_order=True,
        )
        seo_site_browser.page.locator.return_value.is_enabled.assert_called_once()

    def test_parse_data_request_success(self, seo_site_request):
        """
        Scenario: Test successful parsing of data using the request method.
        When successfully parsing data using the request method.
        Then ensure the result value matches the expected response text.
        """
        # Arrange
        mock_response_text = "mock response text"
        mock_page = MagicMock()
        mock_response = MagicMock()
        mock_response.text = mock_response_text
        mock_response.status_code = 200
        mock_page.get.return_value = mock_response
        seo_site_request.request_client.get_client = mock_page
        # Act
        result = seo_site_request.parse_data_request("/example-url")
        # Assert
        assert result.value == mock_response_text

    def test_parse_data_method_browser_success(self, seo_site_browser):
        """
        Scenario: Test successful parsing of data using the browser method.
        When successfully parsing data using the browser method.
        Then ensure the result value matches the expected response text.
        """
        # Arrange
        mock_response = "mock response text"
        mock_page = create_autospec(Page)
        mock_page.goto.return_value = MagicMock()
        mock_page.evaluate.return_value = mock_response
        seo_site_browser.browser_client.get_client = mock_page
        # Act
        result = seo_site_browser.parse_data("/example-url")
        # Assert
        assert result["values"]["value"] == mock_response

    def test_parse_data_method_request_success(self, seo_site_request):
        """
        Scenario: Test successful parsing of data using the request method.
        When successfully parsing data using the request method.
        Then ensure the result value matches the expected response text.
        """
        # Arrange
        mock_response_text = "mock response text"
        mock_page = MagicMock()
        mock_response = MagicMock()
        mock_response.text = mock_response_text
        mock_response.status_code = 200
        mock_page.get.return_value = mock_response
        seo_site_request.request_client.get_client = mock_page
        # Act
        result = seo_site_request.parse_data("/example-url")
        # Assert
        assert result["values"]["value"] == mock_response_text

    @pytest.mark.parametrize(
        "page_exception, expected_error_message",
        [
            (Error("Mock error"), "Unknown `Error`"),
            (NotImplementedError("Mock TimeOutError"), "Mock TimeOutError"),
        ],
    )
    def test_parse_data_method_browser_error(
        self,
        page_exception,
        expected_error_message,
        seo_site_browser,
    ):
        """
        Scenario: Test handling browser error during the parse_data method.
        When encountering a browser error during the parse_data method.
        Then ensure the result error message matches the expected format.
        """
        # Arrange
        mock_page = MagicMock()
        mock_page.goto.side_effect = page_exception
        seo_site_browser.browser_client.get_client = mock_page
        seo_site_browser.browser_client.get_client_without_proxy = mock_page
        # Act
        result = seo_site_browser.parse_data("/example-url")
        # Assert
        assert (
            result["values"]["error"]
            == f"Collect error - {expected_error_message}"
        )
