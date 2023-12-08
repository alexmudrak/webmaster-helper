import pytest

from api.project.models import Project
from api.user.models import User
from mail.models import Mail, MailSettings
from tests.fixtures.project import mock_project
from tests.fixtures.user import mock_user

_ = mock_user, mock_project

mock_mail_data = {
    "mail_settings": MailSettings,
    "mail_box": "mock",
    "mail_id": 0,
    "replay_to": "mock",
    "author_name": "mock",
    "author_mail": "mock",
    "subject": "mock",
    "body": "mock",
    "receive_date": "3333-11-22",
}

mock_mail_setting_data = {
    "owner": User,
    "project": Project,
    "mail_folders": "test-folder",
    "smtp_server": "mock",
    "smtp_port": 1,
    "smtp_username": "mock",
    "smtp_password": "mock",
    "imap_ssl": True,
    "imap_server": "mock",
    "imap_port": 1,
    "imap_username": "mock",
    "imap_password": "mock",
    "check_status": "mock",
}


@pytest.fixture
def mock_mail_box_owner(db, mock_mail_settings) -> User:
    return mock_mail_settings.owner


@pytest.fixture
def mock_mail_settings(db, mock_user, mock_project) -> MailSettings:
    user = mock_user
    mock_mail_setting_data["owner"] = user
    mock_mail_setting_data["project"] = mock_project
    mock_mail_setting_data["smtp_username"] = "mock@mock.1"
    mail_settings = MailSettings.objects.create(**mock_mail_setting_data)
    mock_mail_data["mail_settings"] = mail_settings
    mock_mail_data["mail_id"] = 1
    Mail.objects.create(**mock_mail_data)
    mock_mail_data["mail_id"] = 2
    Mail.objects.create(**mock_mail_data)
    return mail_settings
