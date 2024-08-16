from django.db import models
from viano.files.models import ImageFile, VideoFile
from viano.flows.models import Flow, Stage
from viano.spaces.models import Space

__all__ = [
    "Project",
    "Footage",
]


class Project(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="projects")
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

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __str__(self):
        return self.title


class Footage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="footage"
    )
    video = models.ForeignKey(VideoFile, on_delete=models.CASCADE, related_name="+")
    order = models.IntegerField()
    description = models.TextField()
