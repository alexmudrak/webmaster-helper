import pytest


@pytest.fixture
def mock_os_environ(monkeypatch):
    monkeypatch.setenv("PROXY_SERVER", "mock_proxy_server")
    monkeypatch.setenv("PROXY_USERNAME", "mock_proxy_username")
    monkeypatch.setenv("PROXY_PASSWORD", "mock_proxy_password")


@pytest.fixture
def mock_os_none_environ(monkeypatch):
    monkeypatch.delenv("PROXY_SERVER", raising=False)
    monkeypatch.delenv("PROXY_USERNAME", raising=False)
    monkeypatch.delenv("PROXY_PASSWORD", raising=False)
