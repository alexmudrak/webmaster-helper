import pytest

from api.url.models import Url
from api.url.serializers import UrlSerializer


@pytest.mark.django_db
class TestUrlSerializer:
    def test_invalid_url(self):
        """
        Scenario: Test validation for an invalid URL in the serializer
        When providing an invalid URL to the serializer
        Then the serializer should be marked as not valid with an appropriate
        error
        """
        # Arrange
        data = {"url": "invalidurl"}
        # Act
        serializer = UrlSerializer(data=data)
        # Assert
        assert not serializer.is_valid()
        assert "url" in serializer.errors
        assert serializer.errors["url"][0] == "Enter a valid URL."

    def test_url_without_scheme(self):
        """
        Scenario: Test validation for a URL without a scheme in the serializer
        When providing a URL without a scheme to the serializer
        Then the serializer should be marked as not valid with an appropriate
        error
        """
        # Arrange
        data = {"url": "example.com"}
        # Act
        serializer = UrlSerializer(data=data)
        # Assert
        assert not serializer.is_valid()
        assert "url" in serializer.errors
        assert serializer.errors["url"][0] == "Enter a valid URL."

    def test_url_with_http_scheme(self):
        """
        Scenario: Test validation and normalization for a URL with the HTTP
        scheme in the serializer
        When providing a URL with the HTTP scheme to the serializer
        Then the serializer should be marked as valid, and the URL should be
        normalized
        """
        # Arrange
        data = {"url": "http://EXAMPLE.com"}
        # Act
        serializer = UrlSerializer(data=data)
        # Assert
        assert serializer.is_valid()
        assert serializer.validated_data["url"] == "http://example.com"

    def test_url_with_https_scheme(self):
        """
        Scenario: Test validation and normalization for a URL with the HTTPS
        scheme in the serializer
        When providing a URL with the HTTPS scheme (mixed case) to the
        serializer
        Then the serializer should be marked as valid, and the URL should be
        normalized
        """
        # Arrange
        data = {"url": "https://Example.CoM"}
        # Act
        serializer = UrlSerializer(data=data)
        # Assert
        assert serializer.is_valid()
        assert serializer.validated_data["url"] == "https://example.com"

    def test_valid_url_with_path(self):
        """
        Scenario: Test validation and normalization for a valid URL with a
        path in the serializer
        When providing a valid URL with a path to the serializer
        Then the serializer should be marked as valid, and the URL should be
        normalized without the path
        """
        # Arrange
        data = {"url": "https://example.com/123"}
        # Act
        serializer = UrlSerializer(data=data)
        # Assert
        assert serializer.is_valid()
        assert serializer.validated_data["url"] == "https://example.com"

    def test_serializer_with_existing_url_instance(self):
        """
        Scenario: Test serialization of an existing URL instance
        When providing an existing URL instance to the serializer
        Then the serialized data should contain the URL of the instance
        """
        # Arrange
        url_instance = Url.objects.create(url="https://example.com")
        # Act
        serializer = UrlSerializer(url_instance)
        # Assert
        assert serializer.data["url"] == "https://example.com"
