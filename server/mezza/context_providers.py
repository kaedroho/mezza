from django.urls import reverse

from mezza.models import ProjectStage


def urls(request):
    space = getattr(request, "space", None)
    if not space:
        return {}

    return {
        "projects_index": reverse(
            "projects_index", kwargs={"space_slug": request.space.slug}
        ),
        "projects_create": reverse(
            "projects_create",
            kwargs={"space_slug": request.space.slug, "stage_slug": "stage"},
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


def stages(request):
    space = getattr(request, "space", None)
    if not space:
        return {}

    return [
        {
            "slug": slug,
            "title": title,
            "projects_url": reverse(
                "projects_stage_index", args=[request.space.slug, slug]
            ),
        }
        for slug, title in ProjectStage.choices
    ]
