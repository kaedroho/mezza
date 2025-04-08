from django.db import models

from mezza.auth.models import User

__all__ = [
    "Workspace",
    "WorkspaceUser",
]


class Workspace(models.Model):
    """
    A workspace that provides isolation for multiple tenants.
    """

    name = models.TextField(max_length=50)
    slug = models.TextField(max_length=50, unique=True)
    users = models.ManyToManyField(User, through="WorkspaceUser", related_name="workspaces")


class WorkspaceUser(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="+")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        unique_together = [("workspace", "user")]
