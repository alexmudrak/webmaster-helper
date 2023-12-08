from rest_framework import status

from tests.fixtures.contact import mock_contact, mock_contact_data
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster

_ = (
    mock_user,
    mock_project,
    mock_url,
    mock_contact,
    mock_webmaster,
)


class TestContactViewSet:
    endpoint = "/api/contact/"

    def test_get_contact_list_by_owner(self, client, mock_user, mock_contact):
        """
        Scenario: Get the contact list of User Project
        When after created user, created new project,
        created new few webmasters
        Then trying to get the list of contacts"""
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_get_contact_object_by_owner(
        self, client, mock_user, mock_contact
    ):
        """
        Scenario: Get the contact object of User Project
        When after created user, created new project,
        created new few webmasters
        Then trying to get the object of contact"""
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint + f"{mock_contact.public_id.hex}/")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["type"] == mock_contact_data["type"]

    def test_create_contact_by_owner(self, client, mock_user, mock_contact):
        """
        Scenario: Create a new contact of Webmaster for
        User Project
        When after created user, created new project and
        webmaster
        Then trying to create a new contact and get correct
        response."""
        # Arrange
        data = {
            "type": "Mock contact type 2",
            "contact": "Mock contact",
            "webmaster": {"id": mock_contact.webmaster.public_id},
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.post(self.endpoint, data=data, format="json")
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["type"] == data["type"]

    def test_update_contact_by_owner(self, client, mock_user, mock_contact):
        """
        Scenario: Update contact by owner
        When the client updates a contact object owned by the user
        Then the response should have a status code of HTTP_200_OK,
        and the updated contact should be returned.
        """
        # Arrange
        data = {
            "type": "Change contact type 3",
            "contact": "Mock contact",
            "webmaster": {"id": mock_contact.webmaster.public_id},
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.patch(
            self.endpoint + f"{mock_contact.public_id.hex}/",
            data=data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["type"] == data["type"]
