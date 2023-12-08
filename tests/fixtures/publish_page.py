from datetime import date

import pytest

from api.project.models import Project
from api.webmaster.models import PublishPage, Website
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url, mock_url_data
from tests.fixtures.website import mock_website

_ = mock_website
_ = mock_url
_ = mock_project

publish_page_data = {
    "website": Website,
    "project": Project,
    "url": f"{mock_url_data['url']}/test-publish-page",
    "publish_date": date(2023, 1, 1),
    "check_status": "DONE",
    "check_date": date(2023, 1, 1),
}


@pytest.fixture
def mock_publish_page(db, mock_project, mock_website) -> PublishPage:
    publish_page_data["website"] = mock_website
    publish_page_data["project"] = mock_project
    return PublishPage.objects.create(**publish_page_data)
