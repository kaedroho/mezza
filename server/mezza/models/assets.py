import uuid

from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel

from .files import AudioFile, DocumentFile, ImageFile, VideoFile
from .projects import Project
from .spaces import Space

__all__ = [
    "Asset",
    "ImageAsset",
    "VideoAsset",
    "AudioAsset",
    "DocumentAsset",
]


class Asset(PolymorphicModel):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="assets")
    # If set, the asset belongs to a single project. Otherwise it belongs to the
    # media library
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name="assets"
    )
    title = models.CharField(max_length=255)

    TYPE_NAME = "asset"

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.TYPE_NAME,
            "detail_url": reverse("asset_detail", args=[self.space.slug, self.id]),
        }

    def __str__(self):
        return self.title


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


class ScriptAsset(Asset):
    content = models.JSONField(default=get_default_script)

    TYPE_NAME = "script"

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "type": self.TYPE_NAME,
        }


class ImageAsset(Asset):
    file = models.ForeignKey(
        ImageFile, on_delete=models.CASCADE, related_name="image_assets"
    )

    TYPE_NAME = "image"

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }


class VideoAsset(Asset):
    file = models.ForeignKey(
        VideoFile, on_delete=models.CASCADE, related_name="video_assets"
    )

    TYPE_NAME = "video"

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }


class AudioAsset(Asset):
    file = models.ForeignKey(
        AudioFile, on_delete=models.CASCADE, related_name="audio_assets"
    )

    TYPE_NAME = "audio"

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }


class DocumentAsset(Asset):
    file = models.ForeignKey(
        DocumentFile, on_delete=models.CASCADE, related_name="document_assets"
    )

    TYPE_NAME = "document"

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }
