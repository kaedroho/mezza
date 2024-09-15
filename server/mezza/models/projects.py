import uuid

from django.db import models
from django.urls import reverse

from .spaces import Space

__all__ = [
    "ProjectStage",
    "Project",
]


class ProjectStage(models.TextChoices):
    SCRIPTING = "scripting", "Scripting"
    FILMING = "filming", "Filming"
    EDITING = "editing", "Editing"
    COMPLETED = "completed", "Completed"


def get_default_script():
    def heading(content):
        return {
            "id": uuid.uuid4().hex,
            "type": "heading",
            "props": {
                "level": 3,
                "textColor": "default",
                "textAlignment": "left",
                "backgroundColor": "default",
            },
            "content": [{"text": content, "type": "text", "styles": {}}],
            "children": [],
        }

    def paragraph(content):
        return {
            "id": uuid.uuid4().hex,
            "type": "paragraph",
            "props": {
                "textColor": "default",
                "textAlignment": "left",
                "backgroundColor": "default",
            },
            "content": [{"text": content, "type": "text", "styles": {}}],
        }

    return [
        heading("Introduction"),
        paragraph(""),
        paragraph("... Introduction to the video"),
        paragraph(""),
        heading("Script"),
        paragraph(""),
        paragraph("... Script for the video"),
    ]


class Project(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="projects")
    stage = models.CharField(
        max_length=20, choices=ProjectStage.choices, default=ProjectStage.SCRIPTING
    )
    order = models.IntegerField()
    title = models.TextField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    thumbnail = models.ForeignKey(
        "mezza.ImageFile", on_delete=models.SET_NULL, related_name="+", null=True
    )
    description = models.TextField(blank=True)
    script = models.JSONField(default=get_default_script)
    final_video = models.ForeignKey(
        "mezza.VideoFile", on_delete=models.SET_NULL, related_name="+", null=True
    )

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "stage": {
                "slug": self.stage,
                "title": dict(ProjectStage.choices).get(self.stage, self.stage),
            },
            "detail_url": reverse("project_detail", args=[self.space.slug, self.id]),
            "asset_upload_url": reverse(
                "asset_upload", args=[self.space.slug, self.id]
            ),
        }

    def __str__(self):
        return self.title
