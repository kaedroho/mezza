from django.urls import reverse
from django_bridge.response import Response

from .models import AudioFile, DocumentFile, ImageFile, VideoFile

MEDIA_TYPES = {
    "images": ImageFile,
    "videos": VideoFile,
    "audio": AudioFile,
    "documents": DocumentFile,
}


def index(request, type):
    if type in MEDIA_TYPES:
        files = MEDIA_TYPES[type].objects.all()
    else:
        files = []

    return Response(
        request,
        "MediaIndex",
        {
            "type": type,
            "types": [
                {"name": name, "url": reverse("files_index", args=[name])}
                for name in MEDIA_TYPES.keys()
            ],
            "files": [
                {
                    "id": file.id,
                    "title": file.title,
                    "edit_url": "#",
                    "thumbnail_url": None,
                }
                for file in files
            ],
        },
    )
