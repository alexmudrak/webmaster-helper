import pytest

from api.user.models import User

mock_user_data = {
    "username": "mock_test",
    "email": "mock@email.test",
    "password": "mocktest",
}
mock_user_data_2 = {
    "username": "mock_test_2",
    "email": "mock@email.test_2",
    "password": "mocktest_2",
}


@pytest.fixture
def mock_user(db) -> User:
    return User.objects.create_user(**mock_user_data)


@pytest.fixture
def mock_user_2(db) -> User:
    return User.objects.create_user(**mock_user_data_2)


@pytest.fixture
def mock_superuser(db) -> User:
    return User.objects.create_superuser(**mock_user_data)
