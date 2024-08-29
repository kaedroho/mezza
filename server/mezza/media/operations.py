import filetype

from mezza.models import (
    AudioFile,
    AudioFileAsset,
    DocumentFile,
    DocumentFileAsset,
    ImageFile,
    ImageFileAsset,
    VideoFile,
    VideoFileAsset,
)


def create_file(*, title, file, uploaded_by, space, library=None, project=None):
    mime_type_to_file_model = {}
    for file_model in [AudioFile, DocumentFile, ImageFile, VideoFile]:
        for mime_type in file_model.ALLOWED_FILE_TYPES:
            mime_type_to_file_model[mime_type] = file_model

    file_type = filetype.guess_mime(file)

    if file_type not in mime_type_to_file_model:
        raise ValueError(f"File type '{file_type}' is not supported.")

    file_model = mime_type_to_file_model[file_type]

    file_record = file_model(
        name=file.name, file=file, uploaded_by=uploaded_by, space=space
    )
    file_record._set_metadata(file)
    file_record.save()

    asset_model = {
        AudioFile: AudioFileAsset,
        DocumentFile: DocumentFileAsset,
        ImageFile: ImageFileAsset,
        VideoFile: VideoFileAsset,
    }[file_model]

    return asset_model.objects.create(
        title=title, file=file_record, library=library, project=project
    )
