from django.db import models

from ..models.content import Component, Content
from ..models.workspaces import Workspace

__all__ = [
    "Channel",
    "Posting",
    "BasePost",
    "XPost",
    "FacebookPost",
    "LinkedInPost",
]


class Channel(models.Model):
    url = models.URLField()
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)


class Posting(models.Model):
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="postings"
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="postings"
    )
    posted_at = models.DateTimeField()

    class Meta:
        unique_together = [("content", "channel")]


class BasePost(Component):
    pass

    class Meta:
        abstract = True


class XPost(BasePost):
    text = models.TextField()


class FacebookPost(BasePost):
    body = models.JSONField()


class LinkedInPost(BasePost):
    body = models.JSONField()


class YoutubeVideo(BasePost):
    video = models.ForeignKey("mezzamedia.VideoFile", on_delete=models.PROTECT)
    thumbnail = models.ForeignKey("mezzamedia.ImageFile", on_delete=models.PROTECT)
    description = models.TextField()
