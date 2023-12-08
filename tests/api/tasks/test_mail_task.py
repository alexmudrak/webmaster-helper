from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from api.tasks.mail_task import get_mails, send_mails
from mail.models import Mail
from tests.fixtures.mail_box import mock_mail_settings as mail_settings
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user

_ = mail_settings, mock_user, mock_project, mock_url


@pytest.fixture
def mail_data():
    return {
        "subject": "Test Subject",
        "recipient": "recipient@example.com",
        "message": "Test Message",
    }


@pytest.mark.django_db
class TestMailTask:
    def test_get_mails(self, mail_settings):
        """
        Scenario:
        When the get_mails task is executed for a given mail_settings.
        Then it should initiate the MailApp to collect mail messages and set
        check_status to DONE.
        """
        # Arrange
        fixed_date = timezone.now() - timedelta(days=4)
        Mail.objects.create(
            mail_settings=mail_settings, receive_date=fixed_date
        )

        with patch("api.tasks.mail_task.MailApp") as mock_mail_app:
            # Act
            get_mails(settings_id=mail_settings.id)
            # Assert
            mock_mail_app.return_value.start_collect_mail_messages.assert_called_once()

        mail_settings.refresh_from_db()
        assert mail_settings.check_status == "DONE"

    def test_send_mails(self, mail_settings, mock_project, mail_data):
        """
        Scenario:
        When the send_mails task is executed for a given mail_settings,
        project, and mail_data.
        Then it should initiate the MailApp to send the mail with the provided
        data.
        """
        # Arrange
        with patch("api.tasks.mail_task.MailApp") as mock_mail_app:
            # Act
            send_mails(
                project_id=mock_project.id,
                settings_id=mail_settings.id,
                mail_data=mail_data,
            )
            # Assert
            mock_mail_app.return_value.start_send_mail.assert_called_once_with(
                subject=mail_data["subject"],
                to_email=mail_data["recipient"],
                body=mail_data["message"],
                project=mock_project,
            )
