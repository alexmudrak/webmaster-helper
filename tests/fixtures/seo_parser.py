from unittest.mock import patch

import pytest


@pytest.fixture
def mock_browser_client():
    with patch("seo_parser.core.lib.BrowserClient") as mock_browser_client:
        yield mock_browser_client


@pytest.fixture
def mock_request_client():
    with patch("seo_parser.core.lib.RequestClient") as mock_request_client:
        yield mock_request_client
