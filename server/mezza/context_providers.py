from django.urls import reverse


def urls(request):
    space = getattr(request, "space", None)
    if not space:
        return {}

    return {
        "projects_index": reverse(
            "projects_index", kwargs={"space_slug": request.space.slug}
        ),
        "projects_create": reverse(
            "projects_create", kwargs={"space_slug": request.space.slug}
        ),
        "ideas_index": reverse(
            "ideas_index", kwargs={"space_slug": request.space.slug}
        ),
        "ideas_create": reverse(
            "ideas_create", kwargs={"space_slug": request.space.slug}
        ),
        "asset_index": reverse(
            "asset_index", kwargs={"space_slug": request.space.slug}
        ),
    }


def spaces(request):
    current_space_slug = ""
    current_space = getattr(request, "space", None)
    if current_space:
        current_space_slug = current_space.slug

    return {
        "current": current_space_slug,
        "spaces": [
            {"slug": space.slug, "name": space.name}
            for space in request.user.spaces.all()
        ]
        if request.user.is_authenticated
        else [],
    }
