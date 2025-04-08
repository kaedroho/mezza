from functools import wraps

from django.shortcuts import get_object_or_404

from mezza.workspaces.models import Workspace


def workspace(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        workspace_slug = kwargs.pop("workspace_slug")
        if workspace_slug:
            request.workspace = get_object_or_404(Workspace, slug=workspace_slug)
        else:
            request.workspace = None

        return fn(request, *args, **kwargs)

    return wrapper
