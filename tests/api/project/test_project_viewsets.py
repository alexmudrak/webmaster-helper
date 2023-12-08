from typing import Any

from rest_framework import status

from tests.fixtures.project import Users, owner_and_not_owner, project_owner
from tests.fixtures.url import mock_url
from tests.fixtures.user import User, mock_user, mock_user_2

_ = mock_user, mock_user_2, owner_and_not_owner, project_owner, mock_url


class TestProhandler_mail_settingsjectViewSet:
    endpoint = "/api/project/"

    def test_get_project_list_owner(self, client, project_owner: User):
        """
        Scenario: Test getting list of projects by owner
        When a project owner makes a GET request to the project list endpoint.
        Then the response should have a status code of 200 (HTTP_200_OK)
        and the response data should contain a 'count' key indicating the
        number of projects owned by the user.
        """
        # Arrange
        client.force_authenticate(user=project_owner)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_get_project_list_anonymous(self, client):
        """
        Scenario: Test getting list of projects by anonymous
        When an anonymous user makes a GET request to the project list
        endpoint.
        Then the response should have a status code of
        401 (HTTP_401_UNAUTHORIZED) and the response data should contain a
        'detail' key with the message
        "Authentication credentials were not provided."
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

    def test_get_project_obj_not_owner(
        self, client, owner_and_not_owner: Users
    ):
        """
        Scenario: Test getting list of projects by not owner
        When a user who is not the owner makes a GET request to retrieve a
        specific project.
        Then the response should have a status code of
        403 (HTTP_403_FORBIDDEN).
        """
        # Arrange
        client.force_authenticate(user=owner_and_not_owner.owner)
        response = client.get(self.endpoint)
        project_id = response.data["results"][0]["id"]
        client.force_authenticate(user=owner_and_not_owner.not_owner)
        # Act
        response = client.get(self.endpoint + f"{project_id}/")
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_project_obj_owner(self, client, project_owner: User):
        """
        Scenario: Test getting projects object by owner
        When the owner of a project makes a GET request to retrieve the
        specific project.
        Then the response should have a status code of 200 (HTTP_200_OK),
        and the response data should contain the 'id' matching the requested
        project's id.
        """
        # Arrange
        client.force_authenticate(user=project_owner)
        resp_projects = client.get(self.endpoint)
        project_id = resp_projects.data["results"][0]["id"]
        # Act
        response = client.get(self.endpoint + f"{project_id}/")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == project_id

    def test_create_project_obj_owner(self, client, project_owner: User):
        """
        Scenario: Test creating projects object by owner
        When the owner of a project makes a POST request to create a
        new project.
        Then the response should have a status code of 201 (HTTP_201_CREATED),
        and the response data should match the provided project data.
        """
        # Arrange
        data: dict[str, Any] = {
            "name": "Mock project name",
            "url": {"url": "http://example.com"},
            "mail_settings": {
                "smtp_username": 1,
                "smtp_password": 1,
                "imap_server": 1,
                "imap_username": 1,
                "imap_password": 1,
            },
        }
        client.force_authenticate(user=project_owner)
        # Act
        response = client.post(self.endpoint, data=data, format="json")
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]
        assert response.data["url"] == data["url"]["url"]
        assert response.data["published_count"] == 0
        assert response.data["total_spend"] == 0
        assert response.data["last_published_date"] is None
        assert response.data["mail_settings"] is None

    def test_update_project_obj_owner(self, client, project_owner: User):
        """
        Scenario: Test updating projects object by owner
        When the owner of a project makes a PATCH request to update the
        project details.
        Then the response should have a status code of 200 (HTTP_200_OK),
        and the response data should indicate the successful update with
        the message "Project updated successfully" and the updated project_id.
        """
        # Arrange
        data: dict[str, Any] = {
            "name": "Mock project name",
            "url": {"url": "http://example.com"},
        }
        client.force_authenticate(user=project_owner)
        response = client.post(self.endpoint, data=data, format="json")
        project_id = response.data["id"]
        data["name"] = "Mock project name 2"
        data["url"]["url"] = "https://example-2.com"
        # Act
        response = client.patch(
            self.endpoint + f"{project_id}/", data=data, format="json"
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Project updated successfully"
        assert response.data["project_id"].hex == project_id
