from datetime import datetime
from unittest.mock import patch

from mail.client import MailApp
from tests.fixtures.mail_box import mock_mail_settings
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user

_ = mock_mail_settings, mock_project, mock_user, mock_url


class TestMailClinet:
    @patch("mail.client.MailClient")
    def test_start_collect_mail_messages(
        self, mock_mail_client, mock_mail_settings
    ):
        """
        Scenario: Test the start_collect_mail_messages method of the MailApp
        class.
        When the start_collect_mail_messages method is called with a valid
        start_date_collect,
        Then it should initiate the email collection process using the
        mocked MailClient. The method should pass the correct arguments to the
        get_emails method of the MailClient.
        """
        # Arrange
        mail_app = MailApp(mock_mail_settings)
        mail_app.client.smtp_username = mock_mail_settings.smtp_username
        start_date_collect = datetime.now()
        # Act
        mail_app.start_collect_mail_messages(start_date_collect)
        # Assert
        mail_app.client.get_emails.assert_called_once_with(
            username=mock_mail_settings.smtp_username,
            settings=mock_mail_settings,
            start_date=start_date_collect,
        )

    @patch("mail.client.MailClient")
    def test_start_send_mail(
        self, mock_mail_client, mock_mail_settings, mock_project
    ):
        """
        Scenario: Test the start_send_mail method of the MailApp class.
        When the start_send_mail method is called with valid subject, to_email,
        body, and project parameters,
        Then it should initiate the email sending process using the mocked
        MailClient. The method should pass the correct arguments to the
        send_email method of the MailClient.
        """
        # Arrange
        mail_app = MailApp(mock_mail_settings)
        subject = "Test Subject"
        to_email = "test@example.com"
        body = "Test Body"
        # Act
        mail_app.start_send_mail(subject, to_email, body, mock_project)
        # Assert
        mail_app.client.send_email.assert_called_once_with(
            subject,
            to_email,
            body,
            mock_mail_settings,
            mock_project,
            None,
        )
