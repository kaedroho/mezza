from .models import Workspace, WorkspaceUser


def create_workspace(*, name, slug, users=None):
    return Workspace.objects.create(name=name, slug=slug)


def assign_user_to_workspace(*, user, workspace):
    """
    Assign a user to a workspace.
    """

    return WorkspaceUser.objects.create(user=user, workspace=workspace)
