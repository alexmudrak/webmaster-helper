import pytest

from api.project.models import Project
from api.user.models import User
from api.webmaster.models import Contact, ContactHistory, Webmaster
from api.webmaster.models.website import Website
from tests.fixtures.project import mock_project
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

mock_contact_data = {
    "owner": User,
    "webmaster": Webmaster,
    "type": "Mock contact type",
    "contact": "Mock contact",
}

mock_contact_data_2 = {
    "owner": User,
    "webmaster": Webmaster,
    "type": "Mock contact type 2",
    "contact": "Mock contact 2",
}

mock_contact_history_data = {
    "owner": User,
    "project": Project,
    "webmaster": Webmaster,
    "website": Website,
    "contact": Contact,
    "body": "Mock contact history body",
    "subject": "Mock contact history subject",
}

_ = mock_webmaster, mock_user, mock_website, mock_project


@pytest.fixture
def mock_contact(db, mock_webmaster, mock_user):
    mock_contact_data["webmaster"] = mock_webmaster
    mock_contact_data["owner"] = mock_user
    return Contact.objects.create(
        **mock_contact_data,
    )


@pytest.fixture
def mock_contact_2(db, mock_webmaster, mock_user):
    mock_contact_data_2["webmaster"] = mock_webmaster
    mock_contact_data_2["owner"] = mock_user
    return Contact.objects.create(
        **mock_contact_data_2,
    )


@pytest.fixture
def mock_contact_history(
    db,
    mock_user,
    mock_webmaster,
    mock_website,
    mock_contact,
    mock_project,
):
    mock_contact_history_data["owner"] = mock_user
    mock_contact_history_data["project"] = mock_project
    mock_contact_history_data["webmaster"] = mock_webmaster
    mock_contact_history_data["website"] = mock_website
    mock_contact_history_data["contact"] = mock_contact
    return ContactHistory.objects.create(**mock_contact_history_data)
