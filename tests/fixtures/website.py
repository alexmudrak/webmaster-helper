import pytest

from api.url.models import Url
from api.user.models import User
from api.webmaster.models import Website
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster

website_data_data = {
    "owner": User,
    "url": Url,
    "publish_cost": 1.00,
    "information": "Mock information",
}

_ = mock_user, mock_url, mock_webmaster


@pytest.fixture
def mock_website(db, mock_user, mock_url, mock_webmaster) -> Website:
    user = mock_user
    url = mock_url
    website_data_data["owner"] = user
    website_data_data["url"] = url
    website = Website.objects.create(**website_data_data)
    website.webmaster.set([mock_webmaster])
    return website
