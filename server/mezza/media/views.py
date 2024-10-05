from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from mezza.models import Asset, Project

from .forms import AssetUploadForm
from .operations import FileFormatError, clone_asset, create_file


def asset_index(request):
    assets = Asset.objects.filter(space=request.space, project__isnull=True)

    return Response(
        request,
        "MediaIndex",
        {
            "upload_url": reverse("asset_upload", args=[request.space.slug]),
            "assets": [asset.to_client_representation() for asset in assets],
        },
        title="Asset Library | Mezza Studio",
    )


def asset_detail(request, asset_id):
    asset = Asset.objects.get(space=request.space, id=asset_id)

    return Response(
        request,
        "MediaDetail",
        {
            "asset": asset.to_client_representation(),
        },
        title=f"{asset.title} | Mezza Studio",
        overlay=True,
    )


def asset_upload(request, project_id=None):
    if project_id is not None:
        extra_kwargs = {
            "project": Project.objects.get(space=request.space, id=project_id)
        }
        action_url = reverse("asset_upload", args=[request.space.slug, project_id])
    else:
        extra_kwargs = {}
        action_url = reverse("asset_upload", args=[request.space.slug])

    form = AssetUploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            asset = create_file(
                title=form.cleaned_data["title"],
                file=form.cleaned_data["file"],
                uploaded_by=request.user,
                space=request.space,
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
        title="Upload Asset | Mezza Studio",
    )


def asset_choose_for_project(request, project_id):
    project = Project.objects.get(space=request.space, id=project_id)
    assets = Asset.objects.filter(space=request.space, project__isnull=True)

    if request.method == "POST":
        asset = assets.get(id=request.POST["asset_id"])
        print("PROJECT", project)
        cloned_asset = clone_asset(asset, destination_project=project)

        messages.success(
            request,
            f"Successfully added asset '{cloned_asset.title}' to project '{project.title}'.",
        )

        return HttpResponse()

    return Response(
        request,
        "MediaChooser",
        {
            "action_url": reverse(
                "asset_choose_for_project", args=[request.space.slug, project_id]
            ),
            "assets": [asset.to_client_representation() for asset in assets],
        },
        overlay=True,
        title="Choose Asset | Mezza Studio",
    )
