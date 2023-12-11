from unittest.mock import MagicMock, patch

import pytest

from api.tasks.seo_parse_task import get_seo_metrics
from tests.fixtures.url import mock_url

_ = mock_url


@pytest.fixture
def mock_start_parser():
    return MagicMock()


@pytest.mark.django_db
class TestLinkCheckTask:
    @patch("api.tasks.seo_parse_task.start_parser")
    def test_get_seo_metrics(self, mock_start_parser, mock_url):
        """
        Scenario: Test the get_seo_metrics Celery task.
        When the get_seo_metrics task is executed with a valid url_id,
        Then it should initiate the SEO metrics collection process using
        start_parser.
        After the SEO metrics collection is complete, it should update the Url
        object's seo_check_status to "DONE".
        """
        # Arrange
        url_id = str(mock_url.id)
        mock_start_parser.return_value = None
        # Act
        get_seo_metrics(url_id)
        # Assert
        mock_start_parser.assert_called_once_with(mock_url)
        mock_url.refresh_from_db()
        assert mock_url.seo_check_status == "DONE"
