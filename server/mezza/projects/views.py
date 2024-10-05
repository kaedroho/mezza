from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

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
        return redirect(
            "project_detail", space_slug=request.space.slug, project_id=project_id
        )

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
        "ProjectsListing",
        {
            "projects": [
                project.to_client_representation()
                for project in request.space.projects.all()
            ],
        },
    )


def projects_create(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        create_project(
            title=project.title,
            description=project.description,
            space=request.space,
        )

        messages.success(
            request,
            f"Successfully created project '{project.title}'.",
        )

        return redirect("projects_index", space_slug=request.space.slug)

    return Response(
        request,
        "ProjectsForm",
        {
            "title": "New project",
            "action_url": reverse("projects_create", args=[request.space.slug]),
            "form": form,
        },
        overlay=True,
        title="New Project | Mezza Studio",
    )
