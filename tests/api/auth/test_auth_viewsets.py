import pytest
from rest_framework import status

from tests.fixtures.user import User, mock_user, mock_user_data

_ = mock_user


class TestAuthViewSet:
    endpoint = "/api/auth/"

    def test_login(self, client, mock_user):
        auth_data = {
            "username": mock_user_data["username"],
            "password": mock_user_data["password"],
        }

        response = client.post(self.endpoint + "login/", auth_data)
        assert response.status_code == status.HTTP_200_OK

    def test_login_failed(self, client, mock_user):
        auth_data = {
            "username": mock_user_data["username"],
            "password": mock_user_data["password"] + "wrong",
        }

        response = client.post(self.endpoint + "login/", auth_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.json()["detail"]
            == "No active account found with the given credentials"
        )

    @pytest.mark.django_db
    def test_register(self, client):
        response = client.post(self.endpoint + "register/", mock_user_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_refresh(self, client, mock_user):
        auth_data = {
            "username": mock_user_data["username"],
            "password": mock_user_data["password"],
        }

        response = client.post(self.endpoint + "login/", auth_data)

        assert response.status_code == status.HTTP_200_OK

        auth_refresh = {"refresh": response.data["refresh"]}

        response = client.post(self.endpoint + "refresh/", auth_refresh)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]

    def test_logout(self, client, mock_user: User):
        auth_data = {
            "username": mock_user_data["username"],
            "password": mock_user_data["password"],
        }

        response = client.post(self.endpoint + "login/", auth_data)

        assert response.status_code == status.HTTP_200_OK

        client.force_authenticate(user=mock_user)

        auth_refresh = {"refresh": response.data["refresh"]}

        response = client.post(self.endpoint + "logout/", auth_refresh)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_logout_none_refresh_token(self, client, mock_user: User):
        client.force_authenticate(user=mock_user)

        auth_refresh: dict[str, str] = {}

        response = client.post(self.endpoint + "logout/", auth_refresh)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "A refresh token is required."

    def test_logout_bad_refresh_token(self, client, mock_user: User):
        client.force_authenticate(user=mock_user)

        auth_refresh = {"refresh": "bad_token"}

        response = client.post(self.endpoint + "logout/", auth_refresh)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "The refresh token in invalid."
