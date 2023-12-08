from rest_framework import status

from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user, mock_user_2
from tests.fixtures.webmaster import mock_webmaster

_ = mock_url, mock_user, mock_user_2, mock_project, mock_webmaster


class TestWebmasterViewSet:
    endpoint = "/api/webmaster/"

    def test_get_webmaster_list_by_owner(
        self, client, mock_user, mock_webmaster
    ):
        """
        Scenario: Get the webmasters list of User
        When after created user, created new project,
        created new few webmasters
        Then trying to get the list of webmasters"""
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_get_webmaster_object_by_owner(
        self, client, mock_user, mock_webmaster
    ):
        """
        Scenario: Get the webmaster object of User
        When after created user, created new project,
        created new few webmasters
        Then trying to get the object of webmaster"""
        # Arrange
        client.force_authenticate(user=mock_user)
        objects = client.get(self.endpoint)
        object_id = objects.data["results"][0]["id"]
        # Act
        response = client.get(self.endpoint + f"{object_id}/")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == mock_webmaster.name

    def test_create_webmaster_by_owner(
        self, client, mock_user, mock_webmaster
    ):
        """
        Scenario: Create a new webmasters of User
        When after created user, created new project
        Then trying to create a new webmaster and get
        correct response."""
        # Arrange
        data = {
            "name": mock_webmaster.name,
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.post(self.endpoint, data=data)
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]

    def test_update_webmaster_by_owner(
        self, client, mock_user, mock_webmaster
    ):
        """
        Scenario: Update Webmaster details by the owner
        When the owner, authenticated as mock_user, updates the details of a
        webmaster
        Then the webmaster details should be successfully updated, and the
        response contains the updated information.
        """
        # Arrange
        data = {
            "contacts": [
                {"type": "MOCK TYPE", "contact": "MOCK CONTACT"},
            ],
            "websites": [
                {"site": {"url": "https://new-url.com"}},
            ],
            "payments": [
                {"details": "MOCK DETAILS", "type": "MOCK TYPE"},
            ],
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.patch(
            self.endpoint + f"{mock_webmaster.public_id.hex}/",
            data=data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == mock_webmaster.public_id.hex
        assert response.data["name"] == mock_webmaster.name
        assert response.data["contacts"][0]["type"] == "MOCK TYPE"
        assert response.data["contacts"][0]["contact"] == "MOCK CONTACT"
        assert (
            response.data["websites"][0]["site"]["url"]
            == "https://new-url.com"
        )
        assert response.data["payments"][0]["type"] == "MOCK TYPE"
        assert response.data["payments"][0]["details"] == "MOCK DETAILS"
