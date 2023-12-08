import pytest

from seo_parser.libs import WebArchive
from tests.fixtures.seo_parser import mock_browser_client, mock_request_client

_ = mock_browser_client
_ = mock_request_client


class TestSeoParser:
    @pytest.fixture
    def seo_site_request(self, mock_request_client):
        seo_site = WebArchive(request_client=mock_request_client())
        return seo_site

    def test_serialize_with_value(self, seo_site_request):
        """
        Scenario: Test serialization of WebArchive instance with a specified
        value.
        When setting a value and serialize_data for a WebArchive instance.
        Then call the serialize method. Assert that the serialized result
        matches the expected structure.
        """
        # Arrange
        seo_site_request.value = {"layout": {"mock_key": "mock_value"}}
        seo_site_request.serialize_data = {"key": "data"}
        # Act
        result = seo_site_request.serialize()
        # Assert
        expected_result = {
            "key": "data",
            "values": {
                "newest": None,
                "oldest": None,
                "total": 0,
                "value": 0,
            },
        }
        assert result == expected_result
