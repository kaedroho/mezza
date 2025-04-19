from django.conf import settings
from django.db import models
from django.urls import reverse
from uuid_extensions import uuid7

from mezza.workspaces.models import Workspace

__all__ = ["FileBlob", "File"]


def get_upload_path(instance, filename):
    return f"{instance.workspace.slug}/{filename}"


class FileBlob(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid7)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.PROTECT, related_name="file_blobs"
    )
    file = models.FileField(upload_to=get_upload_path)
    total_size = models.PositiveIntegerField()
    uploaded_size = models.PositiveIntegerField()
    checksum = models.PositiveIntegerField(null=True)
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    attributes = models.JSONField(null=True, blank=True)

    def to_client_representation(self):
        return {
            "size": self.total_size,
            "content_type": self.content_type,
            "attributes": self.attributes,
            "download_url": self.file.url,
        }


class File(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.PROTECT, related_name="files"
    )
    name = models.CharField(max_length=255)
    source_blob = models.ForeignKey(
        FileBlob, on_delete=models.PROTECT, related_name="+"
    )
    thumbnail_blob = models.ForeignKey(
        FileBlob, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        unique_together = [("workspace", "name")]

    def __str__(self):
        return self.name

    def to_client_representation(self):
        return {
            "id": self.id,
            "name": self.name,
            "source_blob": self.source_blob.to_client_representation(),
            "thumbnail_blob": self.thumbnail_blob.to_client_representation()
            if self.thumbnail_blob
            else None,
            "detail_url": reverse("file_detail", args=[self.workspace.slug, self.id]),
        }
