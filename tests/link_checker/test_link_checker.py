from unittest.mock import MagicMock, patch

import pytest
from httpx import ProxyError

from link_checker.checker import start_checker
from tests.fixtures.project import mock_project
from tests.fixtures.publish_page import mock_publish_page
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

_ = (
    mock_publish_page,
    mock_website,
    mock_user,
    mock_url,
    mock_project,
    mock_webmaster,
)


# ruff: noqa: E501
@pytest.mark.django_db
class TestLinkChecker:
    def test_start_checker_success(self, mock_publish_page):
        """
        Scenario: Try to find link on webmaster publish page
        When the start_checker function is called with a mocked publish page.
        Then it should return 1
        """
        # Arrange
        with patch(
            "link_checker.checker.RequestClient"
        ) as mock_request_client:
            mock_request = MagicMock()
            mock_request.get.return_value.text = '<html><body><a href="http://mock.com/link">Link</a></body></html>'
            mock_request_client.return_value.__enter__.return_value.get_client = (
                mock_request
            )
            # Act
            result = start_checker(mock_publish_page)
            # Assert
            assert result == 1

    def test_start_checker_no_links(self, mock_publish_page):
        """
        Scenario: Try to find link on webmaster publish page
        When the start_checker function is called with a mocked publish page
        that contains no links.
        Then it should return 0
        """
        # Arrange
        with patch(
            "link_checker.checker.RequestClient"
        ) as mock_request_client:
            mock_request = MagicMock()
            mock_request.get.return_value.text = "<html><body></body></html>"
            mock_request_client.return_value.__enter__.return_value.get_client = (
                mock_request
            )
            # Act
            result = start_checker(mock_publish_page)
            # Assert
            assert result == 0

    def test_start_checker_proxy_error(self, mock_publish_page, caplog):
        """
        Scenario: Test when getting an exception ProxyError
        When the start_checker function is called with a mocked publish page
        and a simulated ProxyError during the link checking process.
        Then it should log an error message indicating the ProxyError and its
        details.
        """
        # Arrange
        with patch(
            "link_checker.checker.RequestClient"
        ) as mock_request_client:
            mock_request_client.return_value.__enter__.return_value.get_client.get.side_effect = ProxyError(
                "Proxy Error"
            )
            # Act
            start_checker(mock_publish_page)
            # Assert
            assert "For page" in caplog.text
            assert "Error: Proxy Error" in caplog.text
