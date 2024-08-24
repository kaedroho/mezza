from django.contrib import messages
from django.db.models import F
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from ..models import Project, ProjectStage
from .forms import ProjectForm


def projects_index(request):
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    return Response(
        request,
        "ProjectsBoard",
        {
            "stages": [
                {
                    "slug": slug,
                    "title": title,
                }
                for slug, title in ProjectStage.choices
            ],
            "projects": [
                project.to_client_representation() for project in space.projects.all()
            ],
        },
    )


def projects_stage_index(request, stage_slug):
    space = request.user.spaces.first()
    stage_title = dict(ProjectStage.choices)[stage_slug]
    return Response(
        request,
        "ProjectsListing",
        {
            "stage": {"slug": stage_slug, "title": stage_title},
            "projects": [
                project.to_client_representation()
                for project in space.projects.filter(stage=stage_slug)
            ],
        },
    )


def projects_create(request, stage_slug):
    stage_title = dict(ProjectStage.choices)[stage_slug]
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.stage = stage_slug
        project.space = space

        # Order the project at the start of the stage
        project.order = 0
        Project.objects.filter(stage=stage_slug).update(order=F("order") + 1)

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
            "action_url": reverse("projects_create", args=[stage_slug]),
            "form": form,
        },
        overlay=True,
        title="New Project | Mezza Studio",
    )
