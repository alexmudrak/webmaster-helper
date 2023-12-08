from rest_framework import status

from tests.fixtures.project import mock_project
from tests.fixtures.publish_page import mock_publish_page
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

_ = (
    mock_publish_page,
    mock_user,
    mock_project,
    mock_url,
    mock_website,
    mock_webmaster,
)


class TestPublishpageViewSet:
    endpoint = "/api/publish-pages/"

    def test_get_publish_page_list_by_owner(
        self, client, mock_user, mock_publish_page
    ):
        """
        Scenario: Get the list of PublishPage objects owned by the user
        When the client is authenticated as the user
        Then the response should have a status code of HTTP_200_OK,
        and the list of PublishPage objects owned by the user should be
        returned.
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_get_publish_page_object_by_owner(
        self, client, mock_user, mock_publish_page
    ):
        """
        Scenario: Get a specific PublishPage object owned by the user
        When the client is authenticated as the user
        Then the response should have a status code of HTTP_200_OK,
        and the details of the specific PublishPage object owned by the user
        should be returned.
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(
            self.endpoint + f"{mock_publish_page.public_id.hex}/"
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["url"] == mock_publish_page.url
