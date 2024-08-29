from django.contrib import messages
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from mezza.models import Asset, AssetLibrary, Project

from .forms import AssetUploadForm
from .operations import create_file


def asset_index(request, library_id=None):
    if library_id is None:
        library = None
        assets = Asset.objects.all()
    else:
        library = AssetLibrary.objects.get(id=library_id)
        assets = library.assets.all()

    return Response(
        request,
        "MediaIndex",
        {
            "library": library.to_client_representation() if library else None,
            "libraries": [
                other_library.to_client_representation()
                for other_library in AssetLibrary.objects.all()
            ],
            "assets": [
                {
                    "id": asset.id,
                    "title": asset.title,
                }
                for asset in assets
            ],
        },
    )


def asset_upload(request, library_id=None, project_id=None):
    if library_id is not None:
        extra_kwargs = {"library": AssetLibrary.objects.get(id=library_id)}
        action_url = reverse(
            "asset_upload",
            kwargs={"library_id": library_id},
        )
    elif project_id is not None:
        extra_kwargs = {"project": Project.objects.get(id=project_id)}
        action_url = reverse(
            "asset_upload",
            kwargs={"project_id": project_id},
        )
    else:
        raise ValueError("Either library_id or project_id must be provided.")

    form = AssetUploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        asset = create_file(
            title=form.cleaned_data["title"],
            file=form.cleaned_data["file"],
            uploaded_by=request.user,
            space=request.user.spaces.first(),
            **extra_kwargs,
        )

        messages.success(
            request,
            f"Successfully uploaded asset '{asset.title}'.",
        )

        return CloseOverlayResponse(request)

    return Response(
        request,
        "MediaUploadForm",
        {
            "action_url": action_url,
            "form": form,
        },
        overlay=True,
    )
