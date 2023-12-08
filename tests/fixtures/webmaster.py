from dataclasses import dataclass

import pytest

from api.user.models import User
from api.webmaster.models import Webmaster
from tests.fixtures.project import mock_user


@dataclass
class Users:
    owner: User
    not_owner: User


mock_webmaster_data = {
    "owner": User,
    "name": "Mock webmaster",
}

_ = mock_user


@pytest.fixture
def mock_webmaster(db, mock_user):
    mock_webmaster_data["owner"] = mock_user
    return Webmaster.objects.create(
        **mock_webmaster_data,
    )
