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

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.polymorphic_ctype.model,
        }

    def __str__(self):
        return self.title


class ImageAsset(Asset):
    file = models.ForeignKey(
        ImageFile, on_delete=models.CASCADE, related_name="image_assets"
    )

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }


class VideoAsset(Asset):
    file = models.ForeignKey(
        VideoFile, on_delete=models.CASCADE, related_name="video_assets"
    )

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }


class AudioAsset(Asset):
    file = models.ForeignKey(
        AudioFile, on_delete=models.CASCADE, related_name="audio_assets"
    )

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }


class DocumentAsset(Asset):
    file = models.ForeignKey(
        DocumentFile, on_delete=models.CASCADE, related_name="document_assets"
    )

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "file": self.file.to_client_representation(),
        }
