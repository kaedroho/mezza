from django.db import models

from crowflow.files.models import ImageFile, VideoFile
from crowflow.flows.models import Flow, Stage

__all__ = [
    "Project",
]


class Project(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="projects")
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="projects")
    title = models.TextField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    thumbnail = models.ForeignKey(
        ImageFile, on_delete=models.SET_NULL, related_name="+", null=True
    )
    description = models.TextField(blank=True)
    script = models.TextField(blank=True)
    final_video = models.ForeignKey(
        VideoFile, on_delete=models.SET_NULL, related_name="+", null=True
    )


class Footage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="footage"
    )
    video = models.ForeignKey(VideoFile, on_delete=models.CASCADE, related_name="+")
    order = models.IntegerField()
    description = models.TextField()
