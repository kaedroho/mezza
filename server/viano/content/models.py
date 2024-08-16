from django.db import models

from ..spaces.models import Space

__all__ = [
    "Content",
]


class Content(models.Model):
    """
    An individual piece of content. Such as a specific Page, Blog Post, or Video.
    """

    id = models.UUIDField(primary_key=True)
    space = models.ForeignKey(Space, on_delete=models.PROTECT)
    title = models.TextField()
