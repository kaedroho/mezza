import tempfile

import ffmpeg
import filetype
import PyPDF2
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.urls import reverse

from mezza.utils.files import hash_filelike
from mezza.utils.thumbnails import generate_thumbnail

from mezza.workspaces.models import Workspace

__all__ = [
    "File",
]


def get_upload_path(instance, filename):
    return f"{instance.workspace.slug}/{filename}"


class File(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.PROTECT, related_name="files"
    )
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_path)
    size = models.PositiveIntegerField()
    checksum = models.PositiveIntegerField(null=True)
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    attributes = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    def to_client_representation(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "content_type": self.content_type,
            "attributes": self.attributes,
            "download_url": self.file.url,
            "detail_url": reverse("file_detail", args=[self.workspace.slug, self.id]),
        }
