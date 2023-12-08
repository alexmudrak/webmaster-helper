from unittest.mock import MagicMock, patch

import pytest

from api.tasks.link_check_task import get_link_check
from tests.fixtures.project import mock_project
from tests.fixtures.publish_page import mock_publish_page
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

_ = (
    mock_publish_page,
    mock_project,
    mock_user,
    mock_url,
    mock_website,
    mock_webmaster,
)


@pytest.fixture
def mock_start_checker():
    return MagicMock()


@pytest.mark.django_db
class TestLinkCheckTask:
    @patch("api.tasks.link_check_task.start_checker")
    def test_get_link_check(self, mock_start_checker, mock_publish_page):
        """
        Scenario: Test the get_link_check Celery task.
        When the get_link_check task is executed with a valid page_id,
        Then it should initiate the link checking process using start_checker.
        After the link checking is complete, it should update the PublishPage
        object's check_status to "DONE" and set the check_date.
        """
        # Arrange
        page_id = str(mock_publish_page.id)
        mock_start_checker.return_value = None

        # Act
        get_link_check(page_id)

        # Assert
        mock_start_checker.assert_called_once_with(mock_publish_page)
        mock_publish_page.refresh_from_db()
        assert mock_publish_page.check_status == "DONE"
        assert mock_publish_page.check_date is not None
