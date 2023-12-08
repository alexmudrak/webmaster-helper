from unittest.mock import patch

import pytest

from tests.fixtures.os_environ import mock_os_environ, mock_os_none_environ
from utils.request_client import RequestClient

_ = mock_os_environ, mock_os_none_environ


@pytest.fixture
def mock_httpx_client(monkeypatch):
    class MockClient:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def close(self):
            pass

    monkeypatch.setattr("utils.request_client.httpx.Client", MockClient)


@pytest.fixture
def request_client_instance(mock_os_environ, mock_httpx_client):
    return RequestClient()


class TestRequestClient:
    def test_request_client_init_defaults(self, mock_os_none_environ):
        """
        Scenario: Test the default initialization of RequestClient when
        environment variables are set to None.
        When a new RequestClient instance is created with default values.
        Then the instance should have the attributes
        """
        # Arrange
        # Act
        request_client = RequestClient()
        # Assert
        assert request_client.headers is False
        assert not request_client.proxy
        assert request_client.proxy_server is None
        assert request_client.proxy_username is None
        assert request_client.proxy_password is None

    def test_request_client_init_with_options(self):
        """
        Scenario: Test creating a RequestClient instance with specific options.
        When a new RequestClient instance is created with specific options:
          - use_proxy set to True
          - headers set to {"custom": "header"}
        Then the instance should have the following attributes set:
          - headers: {"custom": "header"}
          - proxy: True
        """
        # Arrange
        # Act
        request_client = RequestClient(
            use_proxy=True, headers={"custom": "header"}
        )
        # Assert
        assert request_client.headers == {"custom": "header"}
        assert request_client.proxy

    def test_request_client_enter_exit(self, request_client_instance):
        """
        Scenario: Test entering and exiting the RequestClient context manager.
        When entering and exiting the context manager using a RequestClient
        instance.
        Then the context manager should create an httpx.Client with specified
        options.
        """
        # Arrange
        # Act
        # Assert
        with request_client_instance as client:
            assert client.client.kwargs["proxies"] is None
            assert client.client.kwargs["headers"] is not False
            assert client.client.kwargs["timeout"] == 10.0

    def test_request_client_get_client(self, request_client_instance):
        """
        Scenario: Test getting the httpx.Client instance from the
        RequestClient.
        When getting the httpx.Client instance using the get_client property
        of a RequestClient instance.
        Then the returned httpx.Client instance should be the same as the one
        created in the context manager.
        """
        # Arrange
        # Act
        with request_client_instance as client:
            httpx_client = client.get_client
            # Assert
            assert httpx_client == client.client

    def test_request_client_exit_called_on_exception(
        self, request_client_instance
    ):
        """
        Scenario: Test that the __exit__ method is called on exception in the
        RequestClient context manager.
        When an exception is raised within the context manager using a
        RequestClient instance.
        Then the __exit__ method of the RequestClient should be called.
        """
        # Arrange
        # Act
        with patch.object(RequestClient, "__exit__") as mock_exit:
            with pytest.raises(Exception):
                with request_client_instance:
                    pass
                raise Exception("Test exception")

        # Assert
        mock_exit.assert_called_once()
