from django.db import models
from django.urls import reverse

from .spaces import Space

__all__ = [
    "Idea",
]


class Idea(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="ideas")
    title = models.TextField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField()

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_production_url": reverse("ideas_start_production", args=[self.id]),
        }

    def __str__(self):
        return self.title
