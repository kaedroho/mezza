import tempfile
from io import BytesIO
from math import ceil
from pathlib import Path

import ffmpeg
import filetype
import PyPDF2
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from wand.color import Color
from wand.image import Image as WandImage
from willow.image import Image

from .models import File, FileBlob


class FileFormatError(ValueError):
    pass


def extract_imagefile_attributes(file):
    image = Image.open(file)
    size = image.get_size()

    return {
        "dimensions": {
            "width": size[0],
            "height": size[1],
        }
    }


def extract_audiofile_attributes(file):
    audio_streams = ffmpeg.probe(file.path, select_streams="a")["streams"]

    return {
        "duration": audio_streams[0]["duration"],
        "ffprobe": {"audio_streams": audio_streams},
    }


def extract_videofile_attributes(file):
    video_stream = ffmpeg.probe(file.path, select_streams="v:0", count_frames=None)[
        "streams"
    ][0]
    audio_streams = ffmpeg.probe(file.path, select_streams="a")["streams"]

    return {
        "dimensions": {
            "width": video_stream["width"],
            "height": video_stream["height"],
        },
        "duration": video_stream.get("duration"),
        "ffprobe": {
            "video_stream": video_stream,
            "audio_streams": audio_streams,
        },
    }


def extract_pdffile_attributes(file):
    reader = PyPDF2.PdfReader(file.path)

    return {
        "pages": len(reader.pages),
    }


METADATA_EXTRACTORS = {
    "image/jpeg": extract_imagefile_attributes,
    "image/png": extract_imagefile_attributes,
    "image/gif": extract_imagefile_attributes,
    "image/webp": extract_imagefile_attributes,
    "image/avif": extract_imagefile_attributes,
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


def generate_imagefile_thumbnail(file):
    image = Image.open(file)
    width, height = image.get_size()

    # Generate a thumbnail with height 480 pixels
    new_height = min(height, 480)
    new_width = ceil(width * new_height / height)

    image = image.resize((new_width, new_height))

    output = BytesIO()
    image.save_as_avif(output, 50, False)
    return output


def generate_videofile_thumbnail(file):
    video_stream = ffmpeg.probe(file.path, select_streams="v:0", count_frames=None)[
        "streams"
    ][0]
    width = video_stream["width"]
    height = video_stream["height"]

    # Generate a thumbnail with height 480 pixels
    new_height = min(height, 480)
    new_width = int(ceil(width * new_height / height))

    # Resize the video and remove audio
    with tempfile.TemporaryDirectory() as tmp:
        out_filename = str(Path(tmp) / Path(file.name).with_suffix(".t.webm").name)
        print("OUT", out_filename)
        ffmpeg.input(file.path).output(
            out_filename,
            vf=f"scale={new_width}:{new_height}",
            format="webm",
            an=None,
        ).run(capture_stdout=True)
        return open(out_filename, "rb")


def generate_pdffile_thumbnail(file):
    image = WandImage(filename=file.path + "[0]")
    width, height = image.size

    # Generate a thumbnail with height 240 pixels
    new_height = min(height, 480)
    new_width = ceil(width * new_height / height)

    image.resize(new_width, new_height)
    image.background_color = Color("rgb(255, 255, 255)")
    image.alpha_channel = "remove"

    output = BytesIO()
    with image.convert("avif") as converted:
        converted.compression_quality = 50
        converted.save(file=output)

    return output


THUMBNAIL_GENERATORS = {
    "image/jpeg": generate_imagefile_thumbnail,
    "image/png": generate_imagefile_thumbnail,
    "image/gif": generate_imagefile_thumbnail,
    "image/webp": generate_imagefile_thumbnail,
    "video/mp4": generate_videofile_thumbnail,
    "video/webm": generate_videofile_thumbnail,
    "video/ogg": generate_videofile_thumbnail,
    "video/x-matroska": generate_videofile_thumbnail,
    "video/quicktime": generate_videofile_thumbnail,
    "application/pdf": generate_pdffile_thumbnail,
}


class InvalidFileError(ValueError):
    pass


def create_file(*, name, total_size, uploaded_file, uploaded_by, workspace):
    # validate file size, reject files larger than MAX_UPLOAD_SIZE
    if total_size > settings.MAX_UPLOAD_SIZE:
        raise ValueError("File size is too large.")

    if uploaded_file.size == total_size:
        finalise = True

    elif uploaded_file.size < total_size:
        # Only part of the file has been uploaded,
        # don't perform any processing until the rest is uploaded
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

    file = File.objects.create(workspace=workspace, name=name, source_blob=blob)

    if finalise:
        finalise_file(file=file)

    return file


def append_blob(*, blob, uploaded_file):
    new_uploaded_size = blob.uploaded_size + uploaded_file.size

    if new_uploaded_size == blob.total_size:
        finalise = True

    elif new_uploaded_size < blob.total_size:
        # Only part of the file has been uploaded,
        # don't perform any processing until the rest is uploaded
        finalise = False

    else:
        raise InvalidFileError("Uploaded file is larger than the total file size.")

    # TODO: Append data

    if finalise:
        finalise_blob(blob=blob)

        # Finalise any files that use the blob as a source
        for file in File.objects.filter(source_blob=blob):
            finalise_file(file=file)


def finalise_blob(*, blob):
    if blob.attributes is not None:
        raise ValueError("Blob is already finalised")

    blob.attributes = METADATA_EXTRACTORS[blob.content_type](blob.file)
    blob.save(update_fields=["attributes"])


def finalise_file(*, file):
    if file.source_blob.content_type in THUMBNAIL_GENERATORS:
        thumbnail_data = THUMBNAIL_GENERATORS[file.source_blob.content_type](
            file.source_blob.file
        )

        content_type = filetype.guess(thumbnail_data)

        file_name = Path(file.source_blob.file.name).with_suffix(
            ".t." + content_type.extension
        )
        thumbnail_data.seek(2)
        file_size = thumbnail_data.tell()
        thumbnail_data.seek(0)

        file.thumbnail_blob = FileBlob.objects.create(
            workspace=file.workspace,
            file=ContentFile(thumbnail_data.read(), name=file_name),
            total_size=file_size,
            uploaded_size=file_size,
            checksum=None,  # TODO
            content_type=content_type.mime,
            uploaded_by_id=file.source_blob.uploaded_by_id,
        )

        finalise_blob(blob=file.thumbnail_blob)

        file.save(update_fields=["thumbnail_blob"])
