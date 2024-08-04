from django.db import models

from .workspaces import Workspace

__all__ = [
    "Campaign",
]


class Campaign(models.Model):
    name = models.TextField()
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)
