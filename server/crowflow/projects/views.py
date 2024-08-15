from django.contrib import messages
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from .forms import ProjectForm


def index(request):
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    return Response(
        request,
        "ProjectsIndex",
        {
            "projects": [
                project.to_client_representation() for project in space.projects.all()
            ],
        },
    )


def create(request):
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    form = ProjectForm(space, request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.space = space
        project.save()

        messages.success(
            request,
            f"Successfully created project '{project.title}'.",
        )

        return CloseOverlayResponse(request)

    return Response(
        request,
        "ProjectsForm",
        {
            "action_url": reverse("projects_create"),
            "form": form,
        },
        overlay=True,
        title="Create Project | CrowFlow",
    )
