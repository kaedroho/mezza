from django.urls import reverse

from mezza.models import AssetLibrary, ProjectStage


def urls(request):
    default_asset_library = AssetLibrary.objects.first()
    return {
        "projects_index": reverse("projects_index"),
        "projects_create": reverse("projects_create", args=["stage"]),
        "ideas_index": reverse("ideas_index"),
        "ideas_create": reverse("ideas_create"),
        "asset_index": reverse(
            "asset_index",
            args=[default_asset_library.id if default_asset_library else None],
        ),
    }


def stages(request):
    return [
        {
            "slug": slug,
            "title": title,
            "projects_url": reverse("projects_stage_index", args=[slug]),
        }
        for slug, title in ProjectStage.choices
    ]
