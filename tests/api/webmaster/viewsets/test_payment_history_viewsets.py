from typing import Any

from rest_framework import status

from tests.fixtures.payment import mock_payment, mock_payment_history
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user, mock_user_2
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

_ = (
    mock_user,
    mock_user_2,
    mock_project,
    mock_url,
    mock_payment_history,
    mock_payment,
    mock_webmaster,
    mock_website,
)


class TestPaymentViewSet:
    endpoint = "/api/payment-history/"

    def test_create_payment_history_by_owner(
        self, client, mock_user, mock_payment_history
    ):
        """
        Scenario: Create a new Payment history of Webmaster for
        User Project
        When after created user, created new project and
        webmaster
        Then trying to create a new payment and get correct
        response."""
        # Arrange
        data = mock_payment_history
        data_request: dict[str, Any] = {}
        data_request["website"] = {"id": data.website.public_id.hex}
        data_request["payment"] = {"id": data.payment.public_id.hex}
        data_request["project"] = {"id": data.project.public_id.hex}
        data_request["price"] = 11.11

        client.force_authenticate(user=mock_user)
        # Act
        response = client.post(self.endpoint, data=data_request, format="json")
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["price"] == str(data.price)

    def test_get_payment_history_list_by_owner(
        self, client, mock_user, mock_payment_history
    ):
        """
        Scenario: Get the Payment history list of User Project
        When after created user, created new project,
        created new few webmasters
        Then trying to get the list of payment types"""
        # Arrange
        client.force_authenticate(user=mock_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_get_payment_history_object_by_owner(
        self, client, mock_user, mock_payment_history
    ):
        """
        Scenario: Get the Payment history object of User Project
        When after created user, created new project,
        created new few webmasters
        Then trying to get the object of payment type"""
        # Arrange
        client.force_authenticate(user=mock_user)
        objects = client.get(self.endpoint)
        object_id = objects.data["results"][0]["id"]
        # Act
        response = client.get(self.endpoint + f"{object_id}/")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["price"] == str(mock_payment_history.price)
