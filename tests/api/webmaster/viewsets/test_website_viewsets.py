from unittest.mock import patch

from rest_framework import status

from tests.fixtures.project import mock_project
from tests.fixtures.publish_page import mock_publish_page
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user, mock_user_2
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

_ = (
    mock_url,
    mock_user,
    mock_user_2,
    mock_project,
    mock_website,
    mock_webmaster,
    mock_publish_page,
)


class TestWebsiteViewSet:
    endpoint = "/api/url/"

    def test_get_website_list_by_owner(self, client, mock_user, mock_website):
        """
        Scenario: Get the Website list of User Project
        When after created user, created new project,
        created new few webmasters
        Then trying to get the list of websites
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["id"] == mock_website.public_id.hex

    def test_get_website_object_by_owner(
        self,
        client,
        mock_user,
        mock_website,
        mock_webmaster,
        mock_publish_page,
    ):
        """
        Scenario: Get the Website object of User Project
        When after created user, created new project,
        created new few webmasters
        Then trying to get the object of website
        """
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint + f"{mock_website.public_id.hex}/")
        expected_keys = {"moz", "similarweb", "web_archive", "yandex_x"}
        actual_keys = set(response.data["seo_data"].keys())
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == mock_website.public_id.hex
        assert response.data["information"] == mock_website.information
        assert (
            float(response.data["publish_cost"]) == mock_website.publish_cost
        )
        assert response.data["publish_efficiency"] == 0
        assert (
            expected_keys <= actual_keys
        ), f"Unexpected keys in seo_data: {actual_keys - expected_keys}"
        assert (
            response.data["webmasters"][0]["id"]
            == mock_webmaster.public_id.hex
        )
        assert response.data["webmasters"][0]["name"] == mock_webmaster.name
        assert response.data["site"]["id"] == mock_website.url.public_id.hex
        assert response.data["site"]["url"] == mock_website.url.url
        assert (
            response.data["site"]["seo_status"] == mock_website.url.seo_status
        )

    def test_create_website_by_owner(
        self, client, mock_user, mock_project, mock_publish_page
    ):
        """
        Scenario: Create a new Website of Webmaster for
        User Project
        When after created user, created new project and
        webmaster
        Then trying to create a new Website and get correct
        response.
        """
        # Arrange
        data = {
            "site": {"url": "mock2.com"},
            "projects": [
                {
                    "id": mock_project.public_id.hex,
                    "publish_pages": [
                        {
                            "id": mock_publish_page.public_id.hex,
                            "url": "https://published_page.com/mock-page",
                        },
                    ],
                },
            ],
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.post(self.endpoint, data=data, format="json")
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["site"]["url"] == f'https://{data["site"]["url"]}'

    def test_update_website_by_owner(self, client, mock_user, mock_website):
        """
        Scenario: Partially update a Website by Webmaster for User Project
        When after created user, created new project and webmaster,
        Then trying to partially update the Website and get correct response.
        """
        # Arrange
        data = {
            "site": {"url": "changed-mock-2.com"},
        }
        client.force_authenticate(user=mock_user)
        # Act
        response = client.patch(
            self.endpoint + f"{mock_website.public_id.hex}/",
            data=data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Website updated successfully"
        assert response.data["website_id"] == mock_website.public_id

    @patch("api.webmaster.viewsets.website.get_seo_metrics")
    def test_seo_task_action(self, mock_seo_task, client, mock_website):
        """
        Scenario: Run SEO task for a URL
        When a user initiates the SEO task for a specific URL
        Then the task is triggered, and the response contains relevant
        information.
        """
        # Arrange
        mock_seo_task.delay.return_value.id = 1

        website_id = mock_website.url.public_id.hex
        data = {}
        client.force_authenticate(user=mock_website.owner)
        # Act
        response = client.post(
            f"{self.endpoint}{website_id}/run-seo-task/",
            data=data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.data["url"] == mock_website.url.url
        assert response.data["status"] == "PENDING"
        assert response.data["task_id"] == 1

    @patch("api.webmaster.viewsets.website.get_link_check")
    def test_check_links_task_action(
        self, mock_link_check, client, mock_website, mock_publish_page
    ):
        """
        Scenario: Run Check Links task for a Website
        When a user initiates the Check Links task for a specific Website
        Then the tasks are triggered for each PublishPage, and the response
        contains relevant information.
        """
        # Arrange
        mock_link_check.delay.return_value.id = 1

        website_id = mock_website.public_id.hex
        data = {}
        client.force_authenticate(user=mock_website.owner)
        # Act
        response = client.post(
            f"{self.endpoint}{website_id}/run-check-links/",
            data=data,
            format="json",
        )
        # Assert
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "results" in response.data
        results = response.data["results"]
        assert results[0]["task_id"] == 1

        for result in results:
            assert "url" in result
            assert "status" in result
            assert "task_id" in result
