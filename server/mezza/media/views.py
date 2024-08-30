from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from mezza.models import Asset, Project

from .forms import AssetMetadataForm, AssetUploadForm
from .operations import FileFormatError, create_file


def asset_index(request):
    space = request.user.spaces.first()
    assets = Asset.objects.filter(space=space, project__isnull=True)

    return Response(
        request,
        "MediaIndex",
        {
            "upload_url": reverse("asset_upload"),
            "assets": [asset.to_client_representation() for asset in assets],
        },
    )


def asset_detail(request, asset_id):
    space = request.user.spaces.first()
    asset = Asset.objects.get(space=space, id=asset_id)

    return Response(
        request,
        "MediaDetail",
        {
            "asset": asset.to_client_representation(),
        },
    )


def asset_upload(request, project_id=None):
    if project_id is not None:
        extra_kwargs = {"project": Project.objects.get(id=project_id)}
        action_url = reverse(
            "asset_upload",
            kwargs={"project_id": project_id},
        )
    else:
        extra_kwargs = {}
        action_url = reverse("asset_upload")

    form = AssetUploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            asset = create_file(
                title=form.cleaned_data["title"],
                file=form.cleaned_data["file"],
                uploaded_by=request.user,
                space=request.user.spaces.first(),
                **extra_kwargs,
            )
        except FileFormatError as e:
            form.add_error("file", str(e))
        else:
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
