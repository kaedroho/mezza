from django.db import models

from ..models.content import Component, RepeatableComponent

__all__ = [
    "Project",
    "VideoScript",
    "VideoFootage",
]


class Idea(Component):
    description = models.TextField()


class Project(Component):
    pass


class VideoScript(Component):
    text = models.TextField()


class VideoFootage(RepeatableComponent):
    file = models.ForeignKey("mezzamedia.VideoFile", on_delete=models.PROTECT)
