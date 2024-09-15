from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from ..models import ProjectStage
from .forms import ProjectForm, ProjectScriptForm
from .operations import create_project


def project_detail(request, project_id):
    project = request.space.projects.get(id=project_id)

    basic_info_form = ProjectForm(instance=project, data=request.POST or None)
    script_form = ProjectScriptForm(instance=project, data=request.POST or None)

    if basic_info_form.is_valid() and script_form.is_valid():
        basic_info_form.save()
        script_form.save()
        messages.success(request, "Project updated.")
        return redirect("project_detail", project_id=project_id)

    return Response(
        request,
        "ProjectDetail",
        {
            "project": project.to_client_representation(),
            "basicInfoForm": basic_info_form,
            "scriptForm": script_form,
            "assets": [
                asset.to_client_representation() for asset in project.assets.all()
            ],
        },
    )


def projects_index(request):
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
                project.to_client_representation()
                for project in request.space.projects.all()
            ],
        },
    )


def projects_stage_index(request, stage_slug):
    stage_title = dict(ProjectStage.choices)[stage_slug]
    return Response(
        request,
        "ProjectsListing",
        {
            "stage": {"slug": stage_slug, "title": stage_title},
            "projects": [
                project.to_client_representation()
                for project in request.space.projects.filter(stage=stage_slug)
            ],
        },
    )


def projects_create(request, stage_slug):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        create_project(
            title=project.title,
            description=project.description,
            space=request.space,
            stage=stage_slug,
        )

        messages.success(
            request,
            f"Successfully created project '{project.title}'.",
        )

        return CloseOverlayResponse(request)

    return Response(
        request,
        "ProjectsForm",
        {
            "title": "New project",
            "action_url": reverse("projects_create", args=[stage_slug]),
            "form": form,
        },
        overlay=True,
        title="New Project | Mezza Studio",
    )
