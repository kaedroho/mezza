from django.db import models

from ..models.content import Content
from ..models.workspaces import Workspace

__all__ = [
    "YouTubeChannel",
    "YouTubeVideo",
]


class YouTubeChannel(models.Model):
    url = models.URLField()
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT)


class YouTubeVideo(Content):
    channel = models.ForeignKey(
        YouTubeChannel, on_delete=models.CASCADE, related_name="videos"
    )
    video_file = models.ForeignKey("mezzamedia.VideoFile", on_delete=models.PROTECT)
    thumbnail_file = models.ForeignKey("mezzamedia.ImageFile", on_delete=models.PROTECT)
    description = models.TextField()
