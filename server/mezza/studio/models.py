from django.db import models

from ..models.workspaces import Workspace

__all__ = [
    "Project",
    "VideoProject",
    "VideoScript",
    "VideoFootage",
]


class Idea(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)
    title = models.TextField()
    description = models.TextField()


class Project(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)
    title = models.TextField()


class VideoProject(Project):
    pass


class VideoScript(models.Model):
    project = models.ForeignKey(VideoProject, on_delete=models.PROTECT)
    text = models.TextField()


class VideoFootage(models.Model):
    project = models.ForeignKey(VideoProject, on_delete=models.PROTECT)
    file = models.ForeignKey("mezzamedia.VideoFile", on_delete=models.PROTECT)
