from django.db import models
from polymorphic.models import PolymorphicModel

from .files import AudioFile, DocumentFile, ImageFile, VideoFile
from .projects import Project
from .spaces import Space

__all__ = [
    "AssetLibrary",
    "Asset",
    "ImageFileAsset",
    "VideoFileAsset",
    "AudioFileAsset",
    "DocumentFileAsset",
]


class AssetLibrary(models.Model):
    space = models.ForeignKey(
        Space, on_delete=models.CASCADE, related_name="asset_libraries"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Asset(PolymorphicModel):
    # An asset can belong to either an asset library or a project, but not both.
    library = models.ForeignKey(
        AssetLibrary, on_delete=models.CASCADE, null=True, related_name="assets"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name="assets"
    )
    name = models.CharField(max_length=255)


class ImageFileAsset(Asset):
    file = models.OneToOneField(
        ImageFile, on_delete=models.CASCADE, related_name="image_assets"
    )


class VideoFileAsset(Asset):
    file = models.OneToOneField(
        VideoFile, on_delete=models.CASCADE, related_name="video_assets"
    )


class AudioFileAsset(Asset):
    file = models.OneToOneField(
        AudioFile, on_delete=models.CASCADE, related_name="audio_assets"
    )


class DocumentFileAsset(Asset):
    file = models.OneToOneField(
        DocumentFile, on_delete=models.CASCADE, related_name="document_assets"
    )
