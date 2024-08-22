from django.contrib import messages
from django.db.models import F
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from ..models import Project
from .forms import ProjectForm


def index(request):
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    return Response(
        request,
        "ProjectsIndex",
        {
            "stages": [
                stage.to_client_representation() for stage in space.stages.all()
            ],
            "projects": [
                project.to_client_representation() for project in space.projects.all()
            ],
        },
    )


def create(request, pipeline_slug, stage_id):
    pipeline = request.user.spaces.first().pipelines.get()
    stage = pipeline.stages.get(id=stage_id)
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.pipeline = pipeline
        project.stage = stage
        project.space = space

        # Order the project at the start of the stage
        project.order = 0
        Project.objects.filter(stage=stage).update(order=F("order") + 1)

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
            "action_url": reverse("projects_create", args=[pipeline_slug, stage_id]),
            "form": form,
        },
        overlay=True,
        title="New Project | Mezza Studio",
    )
