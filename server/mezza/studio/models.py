from django.db import models

from ..models.workspaces import Workspace

__all__ = [
    "Project",
]


class Project(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)
    title = models.TextField()
