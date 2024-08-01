from django.contrib.contenttypes.models import ContentType as DjangoContentType
from django.db import models

from .workspaces import Workspace

__all__ = [
    "ContentType",
    "Content",
    "Component",
    "LongFormText",
    "RepeatableComponent",
]


class ContentType(models.Model):
    """
    A type of content. Such as a Page, Blog Post, or Image.
    """

    name = models.TextField(max_length=50)
    slug = models.TextField(max_length=50)
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)
    base = models.ForeignKey(
        DjangoContentType, on_delete=models.CASCADE, related_name="+"
    )
    components = models.ManyToManyField(
        DjangoContentType, through="ContentTypeComponent", related_name="+"
    )

    class Meta:
        unique_together = [("workspace", "slug")]


class ContentTypeComponent(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="+"
    )
    component = models.ForeignKey(
        DjangoContentType, on_delete=models.CASCADE, related_name="+"
    )

    class Meta:
        unique_together = [("content_type", "component")]


class Content(models.Model):
    """
    An individual piece of content. Such as a specific Page, Blog Post, or Video.
    """

    id = models.UUIDField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    title = models.TextField()


class Component(models.Model):
    """
    A component of a piece of content. Such as a title, body, or image.
    """

    content = models.OneToOneField(
        Content, on_delete=models.CASCADE, primary_key=True, related_name="+"
    )

    class Meta:
        abstract = True


class RepeatableComponent(models.Model):
    """
    A component of a piece of content that can be repeated.
    """

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="+")
    sort_order = models.IntegerField()

    class Meta:
        abstract = True


class ShortFormText(Component):
    """
    A component that contains short-form text.
    """

    content = models.JSONField()


class LongFormText(Component):
    """
    A component that contains long-form text.
    """

    content = models.JSONField()
