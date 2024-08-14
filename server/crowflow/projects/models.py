from django.db import models

__all__ = [
    "Project",
]


class Project(models.Model):
    title = models.TextField(max_length=200)
    flow = models.ForeignKey(
        "crowflowflows.Flow", on_delete=models.CASCADE, related_name="projects"
    )
    stage = models.ForeignKey(
        "crowflowflows.Stage", on_delete=models.CASCADE, related_name="projects"
    )
