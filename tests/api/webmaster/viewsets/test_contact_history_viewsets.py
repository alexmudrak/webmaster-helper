from datetime import datetime

from rest_framework import status

from tests.fixtures.contact import (
    mock_contact,
    mock_contact_2,
    mock_contact_history,
)
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

_ = (
    mock_user,
    mock_project,
    mock_webmaster,
    mock_website,
    mock_contact,
    mock_contact_2,
    mock_url,
    mock_contact_history,
)


class TestContactHistoryViewSet:
    endpoint = "/api/messages/"

    def test_get_list_contact_history_by_owner(
        self,
        client,
        mock_user,
        mock_contact_history,
    ):
        """
        Scenario: Test the endpoint for retrieving a list of contact history
        entries owned by the authenticated user. Given an authenticated user
        (`mock_user`) with associated contact history entries.
        When a request is made to the endpoint for retrieving the list of
        contact history entries.
        Then the response should have a status code of 200 (HTTP_200_OK). The
        response data should contain a "count" indicating the number of
        entries (1 in this case). The first entry in the "results" should have
        an "id" matching the public ID of the mocked contact history.
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert (
            response.data["results"][0]["id"]
            == mock_contact_history.public_id.hex
        )

    def test_get_contact_history_object_data_by_owner(
        self,
        client,
        mock_user,
        mock_project,
        mock_webmaster,
        mock_website,
        mock_contact,
        mock_contact_history,
    ):
        """
        Scenario: Test the endpoint for retrieving detailed data of a specific
        contact history entry owned by the authenticated user. Given an
        authenticated user (`mock_user`) with associated contact history
        entries.
        When a request is made to the endpoint to retrieve detailed data of a
        specific contact history entry.
        Then the response should have a status code of 200 (HTTP_200_OK).
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(
            self.endpoint + f"{mock_contact_history.public_id.hex}/"
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == mock_contact_history.public_id.hex
        assert response.data["subject"] == mock_contact_history.subject
        assert response.data["body"] == mock_contact_history.body
        assert (
            datetime.fromisoformat(response.data["created"])
            == mock_contact_history.created
        )
        assert response.data["webmaster"]["id"] == mock_webmaster.public_id.hex
        assert response.data["webmaster"]["name"] == mock_webmaster.name
        assert response.data["contact"]["id"] == mock_contact.public_id.hex
        assert response.data["contact"]["type"] == mock_contact.type
        assert response.data["contact"]["contact"] == mock_contact.contact
        assert response.data["project"]["id"] == mock_project.public_id.hex
        assert response.data["project"]["name"] == mock_project.name
        assert response.data["website"]["id"] == mock_website.public_id.hex
        assert response.data["website"]["name"] == mock_website.url.url
        assert (
            response.data["website"]["site"]["id"]
            == mock_website.url.public_id.hex
        )
        assert response.data["website"]["site"]["url"] == mock_website.url.url
        assert (
            response.data["website"]["site"]["seo_status"]
            == mock_website.url.seo_status
        )

    def test_create_contact_history_by_owner(
        self,
        client,
        mock_user,
        mock_project,
        mock_webmaster,
        mock_website,
        mock_contact,
    ):
        """
        Scenario: Test the endpoint for creating a new contact history entry
        owned by the authenticated user. Given an authenticated user
        (`mock_user`) with associated projects, webmasters, websites,
        and contacts.
        When a request is made to the endpoint to create a new contact history
        entry with valid data.
        Then the response should have a status code of 201 (HTTP_201_CREATED).
        The response data should contain a success message
        ("message": "Message created successfully").
        """
        # Arrange
        data = {
            "project": {"id": mock_project.public_id.hex},
            "webmaster": {"id": mock_webmaster.public_id.hex},
            "website": {"id": mock_website.public_id.hex},
            "contact": {"id": mock_contact.public_id.hex},
            "subject": "Mock message subject",
            "body": "Mock message body",
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.post(self.endpoint, data=data, format="json")
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "Message created successfully"

    def test_update_contact_history_by_owner(
        self,
        client,
        mock_user,
        mock_project,
        mock_webmaster,
        mock_website,
        mock_contact_history,
        mock_contact_2,
    ):
        """
        Scenario: Test the endpoint for updating a contact history entry owned
        by the authenticated user. Given an authenticated user (`mock_user`)
        with associated contact history entries, projects, webmasters,
        websites, and contacts.
        When a request is made to the endpoint to update an existing contact
        history entry with valid data.
        Then the response should have a status code of 200 (HTTP_200_OK). The
        response data should contain a success message
        ("message": "Message updated successfully").
        """
        # Arrange
        data = {
            "contact": {"id": mock_contact_2.public_id.hex},
            "project": {"id": mock_project.public_id.hex},
            "webmaster": {"id": mock_webmaster.public_id.hex},
            "website": {"id": mock_website.public_id.hex},
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.patch(
            self.endpoint + f"{mock_contact_history.public_id.hex}/",
            data=data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Message updated successfully"
