from django.db import models

from .spaces import Space

__all__ = [
    "Stage",
    "Pipeline",
]


class Stage(models.Model):
    title = models.TextField(max_length=200)
    order = models.IntegerField()
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="stages")

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["space", "order"]


class Pipeline(models.Model):
    title = models.TextField(max_length=200)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="pipelines")
    stages = models.ManyToManyField("Stage", related_name="Pipelines")

    def __str__(self):
        return self.title
