from django.db import models

from .files import ImageFile, VideoFile
from .spaces import Space

__all__ = [
    "ProjectStage",
    "Project",
    "Footage",
]


class ProjectStage(models.TextChoices):
    IDEAS = "ideas", "Ideas"
    SCRIPTING = "scripting", "Scripting"
    FILMING = "filming", "Filming"
    EDITING = "editing", "Editing"
    COMPLETED = "completed", "Completed"


class Project(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="projects")
    stage = models.CharField(
        max_length=20, choices=ProjectStage.choices, default=ProjectStage.IDEAS
    )
    order = models.IntegerField()
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
            "stage": {
                "slug": self.stage,
                "title": dict(ProjectStage.choices).get(self.stage, self.stage),
            },
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
