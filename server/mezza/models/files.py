import filetype
from django.conf import settings
from django.db import models

from ..utils.files import hash_filelike
from .spaces import Space

__all__ = [
    "BaseFile",
    "ImageFile",
    "VideoFile",
    "AudioFile",
    "DocumentFile",
]


def get_upload_path(instance, filename):
    return f"{instance.space.slug}/{instance.UPLOAD_TO}/{filename}"


class BaseFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_path)
    size = models.PositiveIntegerField()
    hash = models.CharField(max_length=40)
    file_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    space = models.ForeignKey(Space, on_delete=models.PROTECT)

    UPLOAD_TO = "files"
    ALLOWED_FILE_TYPES = []

    class InvalidFileError(ValueError):
        pass

    def to_client_representation(self):
        return {
            "id": self.id,
            "name": self.name,
            "download_url": self.file.url,
            "size": self.size,
            "file_type": self.file_type,
        }

    def _set_metadata(self, file):
        self.size = file.size
        self.hash = hash_filelike(file)
        self.file_type = filetype.guess_mime(file)

        # validate file size, reject files larger than MAX_UPLOAD_SIZE
        if self.size > settings.MAX_UPLOAD_SIZE:
            raise self.InvalidFileError("File size is too large.")

        if self.file_type is None:
            raise self.InvalidFileError("The file type could not be determined.")

        if self.file_type not in self.ALLOWED_FILE_TYPES:
            raise self.InvalidFileError(
                f"File type '{self.file_type}' is not supported."
            )

    class Meta:
        abstract = True


class ImageFile(BaseFile):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "width": self.width,
            "height": self.height,
        }

    def _set_metadata(self, file):
        super()._set_metadata(file)

        from PIL import Image

        with Image.open(file) as image:
            self.width, self.height = image.size

    UPLOAD_TO = "images"
    ALLOWED_FILE_TYPES = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    ]


class VideoFile(BaseFile):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    duration = models.DurationField()

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "width": self.width,
            "height": self.height,
            "duration": self.duration,
        }

    UPLOAD_TO = "videos"
    ALLOWED_FILE_TYPES = [
        "video/mp4",
        "video/webm",
        "video/ogg",
    ]


class AudioFile(BaseFile):
    duration = models.DurationField()

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "duration": self.duration,
        }

    UPLOAD_TO = "audio"
    ALLOWED_FILE_TYPES = [
        "audio/mpeg",
        "audio/ogg",
        "audio/wav",
    ]


class DocumentFile(BaseFile):
    page_count = models.PositiveIntegerField()

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "page_count": self.page_count,
        }

    UPLOAD_TO = "documents"
    ALLOWED_FILE_TYPES = [
        "application/pdf",
    ]
