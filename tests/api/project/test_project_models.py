import pytest

from api.project.models import Project
from api.url.models import Url
from tests.fixtures.project import mock_project_data
from tests.fixtures.url import mock_url_data
from tests.fixtures.user import mock_user

_ = mock_user


@pytest.mark.django_db
def test_create_project(mock_user):
    user = mock_user
    url = Url.objects.create(**mock_url_data)
    mock_project_data["owner"] = user
    mock_project_data["url"] = url
    project = Project.objects.create(**mock_project_data)
    expect_str = f"<{project.name}> {project.url} - {project.owner}"
    assert str(project) == expect_str
    assert project.name == mock_project_data["name"]
