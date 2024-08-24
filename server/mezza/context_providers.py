from django.urls import reverse

from mezza.models import ProjectStage


def urls(request):
    return {
        "projects_index": reverse("projects_index"),
        "projects_create": reverse("projects_create", args=["stage"]),
        "ideas_index": reverse("ideas_index"),
        "ideas_create": reverse("ideas_create"),
        "files_index": reverse("files_index", args=["images"]),
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
