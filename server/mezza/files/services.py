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
    File, FileBlob
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


def create_file(*, name, total_size, uploaded_file, uploaded_by, workspace):
    # validate file size, reject files larger than MAX_UPLOAD_SIZE
    if total_size > settings.MAX_UPLOAD_SIZE:
        raise ValueError("File size is too large.")

    if uploaded_file.size == total_size:
        finalise = True

    elif uploaded_file.size < total_size:
        # Only part of the file has been uploaded,
        # don't perform any processing until the rest is uploaded
        finalise = False

    else:
        raise InvalidFileError("Uploaded file is larger than the total file size.")

    # validate file type, reject files not in ALLOWED_FILE_TYPES
    content_type = filetype.guess_mime(uploaded_file)

    if content_type is None:
        raise FileFormatError("The file type could not be determined.")

    if content_type not in METADATA_EXTRACTORS:
        raise FileFormatError(f"File type '{content_type}' is not supported.")

    blob = FileBlob.objects.create(
        workspace=workspace,
        file=uploaded_file,
        total_size=total_size,
        uploaded_size=uploaded_file.size,
        checksum=None,  # TODO
        content_type=content_type,
        uploaded_by=uploaded_by,
    )

    if finalise:
        finalise_blob(blob=blob)

    return File.objects.create(
        workspace=workspace,
        name=name,
        source_blob=blob
    )


def append_blob(*, blob, uploaded_file):
    new_uploaded_size = blob.uploaded_size + uploaded_file.size

    if uploaded_file.size == blob.total_size:
        finalise = True

    elif uploaded_file.size < blob.total_size:
        # Only part of the file has been uploaded,
        # don't perform any processing until the rest is uploaded
        finalise = False

    else:
        raise InvalidFileError("Uploaded file is larger than the total file size.")

    # TODO: Append data

    if finalise:
        finalise_blob(blob=blob)


def finalise_blob(*, blob):
    if blob.attributes is not None:
        raise ValueError("Blob is already finalised")

    blob.attributes = METADATA_EXTRACTORS[blob.content_type](blob.file)
    blob.save(update_fields=['attributes'])
