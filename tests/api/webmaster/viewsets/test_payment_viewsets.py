from rest_framework import status

from tests.fixtures.payment import mock_payment, mock_payment_data
from tests.fixtures.project import mock_project
from tests.fixtures.url import mock_url
from tests.fixtures.user import mock_user, mock_user_2
from tests.fixtures.webmaster import mock_webmaster

_ = (
    mock_user,
    mock_user_2,
    mock_project,
    mock_url,
    mock_payment,
    mock_webmaster,
)


class TestPaymentTypeViewSet:
    endpoint = "/api/payment/"

    def test_create_payment_by_owner(
        self,
        client,
        mock_user,
        mock_payment,
    ):
        """
        Scenario: Create a new payment of Webmaster for
        User Project
        When after created user, created new project and
        webmaster
        Then trying to create a new payment type and get correct
        response."""
        # Arrange
        data = mock_payment_data
        data["webmaster"] = mock_payment.webmaster.public_id
        client.force_authenticate(user=mock_user)
        # Act
        response = client.post(self.endpoint, data=data)
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["type"] == data["type"]

    def test_get_payment_list_by_owner(
        self,
        client,
        mock_user,
        mock_payment,
    ):
        """
        Scenario: Get the Payment list of User Project
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

    def test_get_payment_object_by_owner(
        self,
        client,
        mock_user,
        mock_payment,
    ):
        """
        Scenario: Get the Payment object of User Project
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
        assert response.data["type"] == mock_payment_data["type"]
