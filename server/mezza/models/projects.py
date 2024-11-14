from django.db import models
from django.urls import reverse

from .spaces import Space

__all__ = [
    "Project",
]


class Project(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="projects")
    order = models.IntegerField()
    title = models.TextField(max_length=200)
    release_date = models.DateField(null=True, blank=True)
    thumbnail = models.ForeignKey(
        "mezza.ImageFile", on_delete=models.SET_NULL, related_name="+", null=True
    )
    description = models.TextField(blank=True)
    final_video = models.ForeignKey(
        "mezza.VideoFile", on_delete=models.SET_NULL, related_name="+", null=True
    )

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "detail_url": reverse("project_detail", args=[self.space.slug, self.id]),
            "edit_url": reverse("project_edit", args=[self.space.slug, self.id]),
            "asset_upload_url": reverse(
                "asset_upload", args=[self.space.slug, self.id]
            ),
            "asset_choose_url": reverse(
                "asset_choose_for_project", args=[self.space.slug, self.id]
            ),
        }

    def __str__(self):
        return self.title
