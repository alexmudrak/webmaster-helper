from dataclasses import dataclass

import pytest

from api.project.models import Project
from api.url.models import Url
from api.user.models import User
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user, mock_user_2

_ = mock_user, mock_user_2, mock_url

mock_project_data = {
    "name": "Mock Project",
    "url": Url,
}


@dataclass
class Users:
    owner: User
    not_owner: User


@pytest.fixture
def project_owner(db, mock_user, mock_url) -> User:
    mock_project_data["owner"] = mock_user
    mock_project_data["url"] = mock_url
    project = Project.objects.create(**mock_project_data)
    return project.owner


@pytest.fixture
def owner_and_not_owner(db, mock_user, mock_user_2, mock_url) -> Users:
    mock_project_data["owner"] = mock_user
    mock_project_data["url"] = mock_url
    Project.objects.create(**mock_project_data)

    return Users(mock_user, mock_user_2)


@pytest.fixture
def mock_project(db, mock_user, mock_url) -> User:
    mock_project_data["owner"] = mock_user
    mock_project_data["url"] = mock_url
    return Project.objects.create(**mock_project_data)
