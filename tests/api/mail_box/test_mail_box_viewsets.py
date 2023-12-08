from unittest.mock import patch

import pytest
from rest_framework import status

from tests.fixtures.mail_box import mock_mail_box_owner as mail_box_owner
from tests.fixtures.mail_box import mock_mail_settings
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user

_ = mail_box_owner, mock_mail_settings, mock_user, mock_project, mock_url


@pytest.fixture
def authenticated_client(db, client, mock_mail_settings):
    client.force_authenticate(user=mock_mail_settings.owner)
    return client


class TestMailBoxViewSet:
    endpoint = "/api/mails/"

    def test_post_owner(self, authenticated_client, mock_mail_settings):
        """
        Scenario: Attempt to perform a POST request on the endpoint as an owner
        When trying to perform a POST request on the endpoint as an owner
        Then the response status code should be 405 (Method Not Allowed)
        """
        # Arrange
        # Act
        response = authenticated_client.post(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_owner(self, authenticated_client):
        """
        Scenario: Attempt to perform a PATCH request on the endpoint as an
        owner
        When trying to perform a PATCH request on the endpoint as an owner
        Then the response status code should be 405 (Method Not Allowed)
        """
        # Arrange
        # Act
        response = authenticated_client.patch(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_owner(self, authenticated_client):
        """
        Scenario: Attempt to perform a DELETE request on the endpoint as an
        owner
        When trying to perform a DELETE request on the endpoint as an owner
        Then the response status code should be 405 (Method Not Allowed)
        """
        # Arrange
        # Act
        response = authenticated_client.delete(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_get_owner_mails(self, authenticated_client):
        """
        Scenario: Retrieve the list of mails for the authenticated owner
        When trying to retrieve the list of mails for the authenticated owner
        Then the response status code should be 200 (OK) and contain the
        correct count of mails related to authenticated owner user.
        """
        # Arrange
        # Act
        response = authenticated_client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_get_owner_specific_mail(self, authenticated_client):
        """
        Scenario: Retrieve details for a specific mail of the authenticated
        owner
        When trying to retrieve details for a specific mail of the
        authenticated owner
        Then the response status code should be 200 (OK) and contain the
        correct mail details
        """
        # Arrange
        response_mails = authenticated_client.get(self.endpoint)
        mail_id = response_mails.data["results"][0]["id"]

        # Act
        response_detail = authenticated_client.get(
            self.endpoint + f"{mail_id}/"
        )

        # Assert
        assert response_detail.status_code == status.HTTP_200_OK
        assert response_detail.data["id"] == mail_id

    def test_run_get_mails(self, authenticated_client):
        """
        Scenario: Initiate a task to retrieve mails for the authenticated owner
        When initiating a task to retrieve mails for the authenticated owner
        Then the response status code should be 202 (ACCEPTED) and contain the
        correct task details
        """
        # Arrange
        # Mock the get_mails.delay method to simulate a background task
        with patch(
            "api.tasks.mail_task.get_mails.delay"
        ) as mock_get_mails_delay:
            mock_task_id = "mocked_task_id"
            mock_get_mails_delay.return_value.id = mock_task_id

            # Act
            response = authenticated_client.post(
                self.endpoint + "run-get-mails/"
            )

        # Assert
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert len(response.data["mail_box"]) == 1
        assert response.data["task_id"] == mock_task_id

    def test_run_get_mailbox_status(self, authenticated_client):
        """
        Scenario: Retrieve mailbox status information as an owner
        When trying to retrieve mailbox status information as an owner
        Then the response status code should be 202 (Accepted) and contain
        information about mailbox status
        """
        # Arrange
        with patch(
            "api.tasks.mail_task.get_mails.delay"
        ) as mock_get_mails_delay:
            mock_task_id = "mocked_task_id"
            mock_get_mails_delay.return_value.id = mock_task_id

            # Act
            response = authenticated_client.get(
                self.endpoint + "get-mailbox-status/"
            )

        # Assert
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert len(response.data) == 1
