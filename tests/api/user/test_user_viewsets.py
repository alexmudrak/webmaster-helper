from rest_framework import status

from tests.fixtures.user import User, mock_superuser, mock_user

_ = (
    mock_user,
    mock_superuser,
)


class TestUserViewSet:
    endpoint = "/api/user/"

    def test_list(self, client, mock_user: User):
        """
        Scenario: Get a list of items
        When the client, authenticated as mock_user, requests the list of items
        Then the response should have a status code of HTTP_200_OK,
        and the data should contain a count of 1.
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_list_not_authenticate(self, client):
        """
        Scenario: Get a list without authentication
        When the client requests the list of items without authentication
        Then the response should have a status code of HTTP_401_UNAUTHORIZED,
        and the detail in the response should indicate that authentication
        credentials were not provided.
        """
        # Arrange
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.json()["detail"]
            == "Authentication credentials were not provided."
        )

    def test_list_for_super(self, client, mock_superuser: User):
        """
        Scenario: Get a list as a superuser
        When the superuser client requests the list of items
        Then the response should have a status code of HTTP_200_OK,
        and the count in the response data should indicate the number of items.
        """
        # Arrange
        client.force_authenticate(user=mock_superuser)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_user_info(self, client, mock_user: User):
        """
        Scenario: Get user information
        When the client requests information for a specific user
        Then the response should have a status code of HTTP_200_OK,
        and the returned JSON data should include the correct username.
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(f"{self.endpoint}{mock_user.public_id}/")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == mock_user.get_username()

    def test_user_info_not_authenticate(self, client, mock_user: User):
        """
        Scenario: Get user information without authentication
        When the client requests information for a specific user without
        authentication
        Then the response should have a status code of HTTP_401_UNAUTHORIZED,
        and the returned JSON data should indicate the lack of authentication.
        """
        # Arrange
        # Act
        response = client.get(f"{self.endpoint}{mock_user.public_id}/")
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.json()["detail"]
            == "Authentication credentials were not provided."
        )

    def test_update_user_object(self, client, mock_user: User):
        """
        Scenario: Update user object
        When the client updates a user object
        Then the response should have a status code of HTTP_200_OK,
        and the updated user object should be returned.
        """
        # Arrange
        data = {"mail_settings": {"random_key": None}}
        client.force_authenticate(user=mock_user)
        # Act
        response = client.patch(
            self.endpoint + f"{mock_user.public_id.hex}/",
            data=data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["mail_settings"]
