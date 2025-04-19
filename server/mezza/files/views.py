from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from .models import File

from .forms import FileUploadForm
from .services import FileFormatError, create_file


def file_index(request):
    files = File.objects.filter(workspace=request.workspace)

    return Response(
        request,
        "FileIndex",
        {
            "upload_url": reverse("file_upload", args=[request.workspace.slug]),
            "files": [file.to_client_representation() for file in files],
        },
        title="File Library | Mezza",
    )


def file_detail(request, file_id):
    file = File.objects.get(workspace=request.workspace, id=file_id)

    return Response(
        request,
        "FileDetail",
        {
            "file": file.to_client_representation(),
        },
        title=f"{file.name} | Mezza",
        overlay=True,
    )


def file_upload(request):
    form = FileUploadForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            file = create_file(
                name=form.cleaned_data["name"],
                total_size=form.cleaned_data["file"].size,
                uploaded_file=form.cleaned_data["file"],
                uploaded_by=request.user,
                workspace=request.workspace,
            )
        except FileFormatError as e:
            form.add_error("file", str(e))
        else:
            messages.success(
                request,
                f"Successfully uploaded file '{file.name}'.",
            )

            return CloseOverlayResponse(request)

    return Response(
        request,
        "FileUpload",
        {
            "action_url": reverse("file_upload", args=[request.workspace.slug]),
            "form": form,
        },
        overlay=True,
        title="Upload File | Mezza",
    )
