import tempfile

import ffmpeg
import filetype
import PyPDF2
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from PIL import Image

from mezza.utils.files import hash_filelike
from mezza.utils.thumbnails import generate_thumbnail

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
            "thumbnail": self._get_thumbnail(),
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

    def _generate_thumbnail(self):
        pass

    def _get_thumbnail(self):
        return {
            "type": "image",
            "src": "",  # TODO standard fallback image
        }

    class Meta:
        abstract = True


def get_image_thumbnail_upload_path(instance, filename):
    # Add the word "thumb" to the filename before the extension
    filename_parts = filename.split(".")
    filename_parts.insert(-1, "thumb")
    filename = ".".join(filename_parts)
    return f"{instance.space.slug}/{instance.UPLOAD_TO}/{filename}"


class ImageFile(BaseFile):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    thumbnail_file = models.FileField(
        upload_to=get_image_thumbnail_upload_path, null=True
    )

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "width": self.width,
            "height": self.height,
        }

    def _set_metadata(self, file):
        super()._set_metadata(file)

        with Image.open(file) as image:
            self.width, self.height = image.size

        # Generate a thumbnail
        file = generate_thumbnail(self.file, 200, 200)
        self.thumbnail_file = UploadedFile(
            file=file,
            name=self.file.name,
            content_type="image/jpeg",
            size=file.getbuffer().nbytes,
        )

    def _get_thumbnail(self):
        if self.thumbnail_file:
            return {
                "type": "image",
                "src": self.thumbnail_file.url,
            }

        return super()._get_thumbnail()

    UPLOAD_TO = "images"
    ALLOWED_FILE_TYPES = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    ]


def get_video_thumbnail_upload_path(instance, filename):
    # Set the extension to .thumb.webm
    filename_parts = filename.split(".")
    filename_parts.insert(-1, "thumb")
    filename_parts[-1] = "webm"
    filename = ".".join(filename_parts)
    return f"{instance.space.slug}/{instance.UPLOAD_TO}/{filename}"


class VideoFile(BaseFile):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    video_stream = models.JSONField()
    audio_streams = models.JSONField()
    thumbnail_file = models.FileField(
        upload_to=get_video_thumbnail_upload_path, null=True
    )

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "width": self.width,
            "height": self.height,
            "video_stream": self.video_stream,
            "audio_streams": self.audio_streams,
        }

    def _set_metadata(self, file):
        super()._set_metadata(file)

        with tempfile.NamedTemporaryFile() as tfile, tempfile.TemporaryDirectory() as tmp:
            tfile.write(file.read())
            tfile.flush()
            file.seek(0)

            self.video_stream = ffmpeg.probe(
                tfile.name, select_streams="v:0", count_frames=None
            )["streams"][0]
            self.audio_streams = ffmpeg.probe(tfile.name, select_streams="a")["streams"]
            self.width = int(self.video_stream["width"])
            self.height = int(self.video_stream["height"])

            # Recode video as a 200x200px webm video and remove audio
            tfile.seek(0)
            out_filename = tmp + "/thumbnail.webm"
            ffmpeg.input(tfile.name).output(
                out_filename,
                vf="scale=200:200",
                format="webm",
                an=None,
            ).run(capture_stdout=True)
            outfile = open(out_filename, "rb")

            # Get file size
            outfile.seek(0, 2)
            size = outfile.tell()
            outfile.seek(0)

            self.thumbnail_file = UploadedFile(
                file=outfile,
                name=self.file.name,
                content_type="video/webm",
                size=size,
            )

    def _get_thumbnail(self):
        if self.thumbnail_file:
            return {
                "type": "video",
                "src": self.thumbnail_file.url,
            }

        return super()._get_thumbnail()

    UPLOAD_TO = "videos"
    ALLOWED_FILE_TYPES = [
        "video/mp4",
        "video/webm",
        "video/ogg",
        "video/x-matroska",
        "video/quicktime",
    ]


class AudioFile(BaseFile):
    audio_streams = models.JSONField()

    def _set_metadata(self, file):
        super()._set_metadata(file)

        with tempfile.NamedTemporaryFile() as tfile:
            tfile.write(file.read(1024 * 1024))
            tfile.flush()
            file.seek(0)

            self.audio_streams = ffmpeg.probe(tfile.name, select_streams="a")["streams"]

    UPLOAD_TO = "audio"
    ALLOWED_FILE_TYPES = [
        "audio/mpeg",
        "audio/ogg",
        "audio/wav",
    ]


class DocumentFile(BaseFile):
    page_count = models.PositiveIntegerField()

    def _set_metadata(self, file):
        super()._set_metadata(file)

        reader = PyPDF2.PdfReader(file)
        self.page_count = len(reader.pages)

    def to_client_representation(self):
        return {
            **super().to_client_representation(),
            "page_count": self.page_count,
        }

    UPLOAD_TO = "documents"
    ALLOWED_FILE_TYPES = [
        "application/pdf",
    ]
