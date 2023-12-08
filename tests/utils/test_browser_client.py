from unittest.mock import MagicMock, patch

import pytest
from playwright.sync_api import Page

from tests.fixtures.os_environ import mock_os_environ
from utils.browser_client import BrowserClient

_ = mock_os_environ


@pytest.fixture
def mock_playwright():
    with patch("utils.browser_client.sync_playwright") as mock_playwright:
        yield mock_playwright


@pytest.fixture
def mock_page():
    return MagicMock(spec=Page)


@pytest.fixture
def browser_client_instance(mock_os_environ, mock_playwright):
    return BrowserClient()


class TestBrowserClient:
    def test_browser_client_default_values(self, browser_client_instance):
        """
        Scenario: Test the default values of the BrowserClient instance.
        When a new BrowserClient instance is created with default values.
        Then the instance should have the following attributes set:
          - headless: True
          - proxy: False
          - proxy_server: "mock_proxy_server"
          - proxy_username: "mock_proxy_username"
          - proxy_password: "mock_proxy_password"
        """
        # Arrange
        # Act
        # Assert
        assert browser_client_instance.headless is True
        assert browser_client_instance.proxy is False
        assert browser_client_instance.proxy_server == "mock_proxy_server"
        assert browser_client_instance.proxy_username == "mock_proxy_username"
        assert browser_client_instance.proxy_password == "mock_proxy_password"

    def test_browser_client_with_options(self):
        """
        Scenario: Test creating a BrowserClient instance with specific options.
        When a new BrowserClient instance is created with specific options:
          - headless set to False
          - use_proxy set to True
        Then the instance should have the following attributes set:
          - headless: False
          - proxy: True
        """
        # Arrange
        # Act
        browser_client_instance = BrowserClient(headless=False, use_proxy=True)
        # Assert
        assert browser_client_instance.headless is False
        assert browser_client_instance.proxy is True

    def test_browser_client_enter_exit(
        self, browser_client_instance, mock_page
    ):
        """
        Scenario: Test entering and exiting the BrowserClient context manager.
        When entering and exiting the context manager using a BrowserClient
        instance.
        Then the context manager should launch Chromium with specified options
        and stop Playwright.
        """
        # Arrange
        # Act
        with patch("utils.browser_client.stealth_sync"):
            with browser_client_instance as client:
                # Assert
                client.playwright.chromium.launch.assert_called_once_with(
                    headless=True,
                    proxy=None,
                    handle_sigint=False,
                    handle_sigterm=False,
                    handle_sighup=False,
                    args=["--disable-blink-features=AutomationControlled"],
                )

        client.playwright.stop.assert_called_once()

    def test_browser_client_get_client(
        self, browser_client_instance, mock_page
    ):
        """
        Scenario: Test getting a Playwright Page instance from the
        BrowserClient.
        When getting a Playwright Page instance using the get_client property
        of a BrowserClient instance.
        Then the returned Page instance should be synchronized with stealth
        options.
        """
        # Arrange
        with patch("utils.browser_client.stealth_sync") as mock_stealth_sync:
            with browser_client_instance as client:
                client.client.new_page.return_value = mock_page
                # Act
                page = client.get_client
                # Assert
                mock_stealth_sync.assert_called_once_with(mock_page)
                client.client.new_page.assert_called_once()
                assert page == mock_page

    # ruff: noqa: E501
    def test_browser_client_get_client_without_proxy(
        self, browser_client_instance, mock_page
    ):
        """
        Scenario: Test getting a Playwright Page instance without using a
        proxy from the BrowserClient.
        When getting a Playwright Page instance without using a proxy using
        the get_client_without_proxy property of a BrowserClient instance.
        Then the returned Page instance should be synchronized with stealth
        options.
        """
        # Arrange
        with patch("utils.browser_client.stealth_sync") as mock_stealth_sync:
            with browser_client_instance as client:
                client.playwright.chromium.launch.return_value.new_context.return_value.new_page.return_value = (
                    mock_page
                )
                # Act
                page = client.get_client_without_proxy
                # Assert
                mock_stealth_sync.assert_called_once_with(mock_page)
                client.client.new_context.assert_called_once()
                client.client.new_context.return_value.new_page.assert_called_once()
                assert page == mock_page
