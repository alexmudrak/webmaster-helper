from django.db import models

from api.abstract.models import AbstarctManager, AbstractModel


class ProjectManager(AbstarctManager):
    def create(self, *args, **kwargs) -> "Project":
        return super().create(*args, **kwargs)


class Project(AbstractModel):
    owner = models.ForeignKey(
        to="user.User", on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=255)
    url = models.ForeignKey(
        to="url.Url",
        on_delete=models.SET_NULL,
        null=True,
        related_name="project_url",
    )
    description = models.TextField(blank=True)

    objects = ProjectManager()

    def __str__(self):
        return f"<{self.name}> {self.url} - {self.owner}"

    class Meta:
        unique_together = ("url", "owner")
        db_table = "projects"
