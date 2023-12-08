import pytest

from api.project.models import Project
from api.user.models import User
from api.webmaster.models import Payment, PaymentHistory, Webmaster, Website
from tests.fixtures.project import mock_project
from tests.fixtures.user import mock_user
from tests.fixtures.webmaster import mock_webmaster
from tests.fixtures.website import mock_website

mock_payment_data = {
    "owner": User,
    "webmaster": Webmaster,
    "type": "Other",
    "details": "Mock payment details",
    "description": "Mock payment description",
}

mock_payment_history_data = {
    "owner": User,
    "website": Website,
    "payment": Payment,
    "project": Project,
    "price": 11.11,
    "description": "Mock payment description",
}

_ = mock_project, mock_webmaster, mock_website, mock_user


@pytest.fixture
def mock_payment(db, mock_webmaster, mock_user):
    mock_payment_data["owner"] = mock_user
    mock_payment_data["webmaster"] = mock_webmaster
    return Payment.objects.create(
        **mock_payment_data,
    )


@pytest.fixture
def mock_payment_history(
    db, mock_payment, mock_project, mock_website, mock_user
):
    mock_payment_history_data["owner"] = mock_user
    mock_payment_history_data["website"] = mock_website
    mock_payment_history_data["payment"] = mock_payment
    mock_payment_history_data["project"] = mock_project
    return PaymentHistory.objects.create(
        **mock_payment_history_data,
    )
