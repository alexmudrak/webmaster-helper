import pytest

from api.user.models import User
from tests.fixtures.user import mock_user_data


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(**mock_user_data)
    expected_str = f"{user.username} ({user.email})"
    assert str(user) == expected_str
    assert user.username == mock_user_data["username"]
    assert user.email == mock_user_data["email"]
    assert user.is_active is True


def test_create_user_exception_username():
    not_valid_user = {}

    with pytest.raises(TypeError) as excinfo:
        User.objects.create_user(**not_valid_user)

    assert "Require value for `username`." in str(excinfo)


def test_create_user_exception_email():
    not_valid_user = {
        "username": "mock_username",
    }

    with pytest.raises(TypeError) as excinfo:
        User.objects.create_user(**not_valid_user)

    assert "Require value for `email`." in str(excinfo)


def test_create_user_exception_password():
    not_valid_user = {
        "username": "mock_username",
        "email": "mock@email.com",
    }

    with pytest.raises(TypeError) as excinfo:
        User.objects.create_user(**not_valid_user)

    assert "Require value for `password`." in str(excinfo)


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(**mock_user_data)
    assert user.username == mock_user_data["username"]
    assert user.email == mock_user_data["email"]
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True


def test_create_superuser_exception_username():
    not_valid_user = {}

    with pytest.raises(TypeError) as excinfo:
        User.objects.create_superuser(**not_valid_user)

    assert "Require value for `username`." in str(excinfo)


def test_create_superuser_exception_email():
    not_valid_user = {
        "username": "mock_username",
    }

    with pytest.raises(TypeError) as excinfo:
        User.objects.create_superuser(**not_valid_user)

    assert "Require value for `email`." in str(excinfo)


def test_create_superuser_exception_password():
    not_valid_user = {
        "username": "mock_username",
        "email": "mock@email.com",
    }

    with pytest.raises(TypeError) as excinfo:
        User.objects.create_superuser(**not_valid_user)

    assert "Require value for `password`." in str(excinfo)
