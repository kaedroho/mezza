from django.urls import reverse

from .models import Pipeline


def urls(request):
    return {
        "projects_index": reverse("projects_index"),
        "projects_create": reverse("projects_create", args=["flow", "stage"]),
    }


def pipelines(request):
    # TODO: Filter pipelines by current space
    return [
        {
            "id": pipeline.id,
            "title": pipeline.title,
            "stages": [
                {
                    "id": stage.id,
                    "title": stage.title,
                    "url": reverse("projects_create", args=[pipeline.id, stage.id]),
                }
                for stage in pipeline.stages.all()
            ],
        }
        for pipeline in Pipeline.objects.all()
    ]
