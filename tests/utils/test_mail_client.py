from datetime import datetime
from unittest.mock import patch

import pytest

from api.project.models import Project
from mail.models import MailSettings
from utils.mail_client import MailClient
from utils.types import MailMessage


@pytest.fixture
def mock_smtp_lib():
    with patch("smtplib.SMTP") as mock_smtp:
        yield mock_smtp


@pytest.fixture
def mock_imap_lib():
    with patch("imaplib.IMAP4_SSL") as mock_imap:
        yield mock_imap


@pytest.fixture
def mail_client_settings():
    return {
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "smtp_username": "user@example.com",
        "smtp_password": "password",
        "imap_ssl": True,
        "imap_server": "imap.example.com",
        "imap_port": 993,
        "imap_username": "user@example.com",
        "imap_password": "password",
    }


@pytest.mark.django_db
class TestMailClient:
    def test_send_email(self, mock_smtp_lib, mail_client_settings):
        """
        Scenario: Test the send_email method of the MailClient class.
        When send_email method is invoked with a subject, recipient email,
        body, mail settings, and project
        Then SMTP library should be called, sendmail method of the SMTP library
        should be called
        """
        # Arrange
        subject = "Test Subject"
        to_email = "recipient@example.com"
        body = "Test Body"
        mail_settings = MailSettings.objects.create(**mail_client_settings)
        project = Project.objects.create(name="Test Project")

        # Act
        mail_client = MailClient(**mail_client_settings)
        mail_client.send_email(subject, to_email, body, mail_settings, project)

        # Assert
        assert mock_smtp_lib.called
        assert mock_smtp_lib.return_value.sendmail.called

    # ruff: noqa: E501
    def test_get_emails(self, mock_imap_lib, mail_client_settings):
        """
        Scenario: Test the get_emails method of the MailClient class
        When get_emails method is called with specified parameters, mail client
        is expected to interact with the IMAP library to retrieve emails
        Then get_emails method is invoked with a username, mail settings, and a
        start date
        """
        # Arrange
        username = "user@example.com"
        settings = MailSettings.objects.create(**mail_client_settings)
        start_date = datetime(2023, 1, 1)

        # Mocking IMAP server responses
        mock_imap = mock_imap_lib.return_value
        mock_imap.select.return_value = ("OK", b"1")
        mock_imap.search.return_value = ("OK", [b"1 2 3"])
        mock_imap.fetch.side_effect = [
            (
                "OK",
                [
                    (
                        None,
                        b"Content-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=utf-8\r\nReferences:  <mock_reference>\r\nTo: <mock@example.com>\r\nReply-To: <mock_replay@example.com>\r\nFrom: <mock_from@example.com>\r\nSubject: mock_subject_1\r\nMime-Version: 1.0\r\nMessage-Id: <mock_id_1>\r\nDate: Thu, 30 Nov 2023 00:00:00 +0000\r\n\r\nmock_email data 1.",
                    )
                ],
            ),
            (
                "OK",
                [
                    (
                        None,
                        b"Content-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=utf-8\r\nReferences:  <mock_reference>\r\nTo: <mock@example.com>\r\nReply-To: <mock_replay@example.com>\r\nFrom: <mock_from@example.com>\r\nSubject: mock_subject_1\r\nMime-Version: 1.0\r\nMessage-Id: <mock_id_2>\r\nDate: Thu, 30 Nov 2023 00:00:00 +0000\r\n\r\nmock_email data 2.",
                    )
                ],
            ),
            (
                "OK",
                [
                    (
                        None,
                        b"Content-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=utf-8\r\nReferences:  <mock_reference>\r\nTo: <mock@example.com>\r\nReply-To: <mock_replay@example.com>\r\nFrom: <mock_from@example.com>\r\nSubject: mock_subject_1\r\nMime-Version: 1.0\r\nMessage-Id: <mock_id_3>\r\nDate: Thu, 30 Nov 2023 00:00:00 +0000\r\n\r\nmock_email data 3.",
                    )
                ],
            ),
        ]

        # Act
        mail_client = MailClient(**mail_client_settings)
        result = mail_client.get_emails(username, settings, start_date)

        # Assert
        assert mock_imap_lib.called
        assert mock_imap_lib.return_value.login.called
        assert mock_imap_lib.return_value.select.called
        assert mock_imap_lib.return_value.search.called
        assert mock_imap_lib.return_value.fetch.called

        assert len(result) == 3
        assert isinstance(result[0], MailMessage)
