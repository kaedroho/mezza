import filetype
from PIL import Image

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

from mezza.workspaces.models import Workspace

from .models import (
    File
)


class FileFormatError(ValueError):
    pass


def extract_imagefile_attributes(file):
    with Image.open(file) as image:
        return {
            "width": image.size[0],
            "height": image.size[1],
        }


def extract_audiofile_attributes(file):
    with tempfile.NamedTemporaryFile() as tfile:
        tfile.write(file.read(1024 * 1024))
        tfile.flush()
        file.seek(0)

        audio_streams = ffmpeg.probe(tfile.name, select_streams="a")["streams"]

        return {
            "audio_streams": audio_streams,
        }


def extract_videofile_attributes(file):
    with tempfile.NamedTemporaryFile() as tfile, tempfile.TemporaryDirectory() as tmp:
        tfile.write(file.read())
        tfile.flush()
        file.seek(0)

        video_stream = ffmpeg.probe(tfile.name, select_streams="v:0", count_frames=None)["streams"][0]
        audio_streams = ffmpeg.probe(tfile.name, select_streams="a")["streams"]

        return {
            "video_stream": video_stream,
            "audio_streams": audio_streams,
        }


def extract_pdffile_attributes(file):
    with tempfile.NamedTemporaryFile() as tfile:
        tfile.write(file.read(1024 * 1024))
        tfile.flush()
        file.seek(0)

        reader = PyPDF2.PdfReader(tfile.name)
        return {
            "pages": len(reader.pages),
        }


METADATA_EXTRACTORS = {
    "image/jpeg": extract_imagefile_attributes,
    "image/png": extract_imagefile_attributes,
    "image/gif": extract_imagefile_attributes,
    "image/webp": extract_imagefile_attributes,
    "audio/mpeg": extract_audiofile_attributes,
    "audio/ogg": extract_audiofile_attributes,
    "audio/x-wav": extract_audiofile_attributes,
    "video/mp4": extract_videofile_attributes,
    "video/webm": extract_videofile_attributes,
    "video/ogg": extract_videofile_attributes,
    "video/x-matroska": extract_videofile_attributes,
    "video/quicktime": extract_videofile_attributes,
    "application/pdf": extract_pdffile_attributes,
}


def create_file(*, name, file, uploaded_by, workspace, project=None):
    # validate file size, reject files larger than MAX_UPLOAD_SIZE
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise InvalidFileError("File size is too large.")

    # validate file type, reject files not in ALLOWED_FILE_TYPES
    content_type = filetype.guess_mime(file)

    if content_type is None:
        raise FileFormatError("The file type could not be determined.")

    if content_type not in METADATA_EXTRACTORS:
        raise FileFormatError(f"File type '{content_type}' is not supported.")

    file_metadata_extractor = METADATA_EXTRACTORS[content_type]

    return File.objects.create(
        workspace=workspace,
        name=name,
        file=file,
        uploaded_by=uploaded_by,
        size=file.size,
        content_type=content_type,
        #checksum=hash_filelike(file), TODO checksum
        attributes=file_metadata_extractor(file),
    )
