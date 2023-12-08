import pytest

from api.url.models import Url

mock_url_data = {"url": "http://mock.com"}


@pytest.fixture
def mock_url(db) -> Url:
    return Url.objects.create(**mock_url_data)
