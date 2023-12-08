import pytest
from django.db.utils import IntegrityError

from api.url.models import Url


@pytest.mark.django_db
class TestUrlModel:
    def test_create_url(self):
        """
        Scenario: Test creating a new URL instance
        When a new URL instance is created with a valid URL and SEO status
        Then the instance should have the correct URL, SEO status, and domain
        """
        # Arrange
        url = "https://example.com"
        seo_status = "IN_PROGRESS"
        # Act
        created_url = Url.objects.create(url=url, seo_status=seo_status)
        # Assert
        assert created_url.url == url
        assert created_url.seo_status == seo_status
        assert created_url.domain == "example.com"

    def test_create_duplicate_url(self):
        """
        Scenario: Test creating a duplicate URL instance
        When attempting to create a new URL instance with a URL that already
        exists
        Then an IntegrityError should be raised
        """
        # Arrange
        url = "https://example.com"
        seo_status = "IN_PROGRESS"
        # Act
        Url.objects.create(url=url, seo_status=seo_status)
        # Assert
        with pytest.raises(IntegrityError):
            Url.objects.create(url=url, seo_status=seo_status)

    def test_get_object_by_domain(self):
        """
        Scenario: Test retrieving a URL instance by its domain
        When attempting to retrieve a URL instance using its domain
        Then the correct URL instance should be returned
        """
        # Arrange
        url = "https://example.com"
        seo_status = "IN_PROGRESS"
        created_url = Url.objects.create(url=url, seo_status=seo_status)
        # Act
        retrieved_url = Url.objects.get_object_by_domain(domain="example.com")
        # Assert
        assert retrieved_url == created_url
