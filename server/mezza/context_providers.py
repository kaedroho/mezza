from django.urls import reverse


def urls(request):
    space = getattr(request, "workspace", None)
    if not space:
        return {}

    return {
        "file_index": reverse(
            "file_index", kwargs={"workspace_slug": request.workspace.slug}
        ),
    }


def workspaces(request):
    current_workspace_slug = ""
    current_workspace = getattr(request, "workspace", None)
    if current_workspace:
        current_workspace_slug = current_workspace.slug

    return {
        "current": current_workspace_slug,
        "workspaces": [
            {"slug": workspace.slug, "name": workspace.name}
            for workspace in request.user.workspaces.all()
        ]
        if request.user.is_authenticated
        else [],
    }
