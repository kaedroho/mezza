from django.db import models

from mezza.auth.models import User


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    status = models.CharField(max_length=9, choices=Status.choices)
    content = models.JSONField()
