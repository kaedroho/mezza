from django.urls import reverse


def urls(request):
    return {
        "projects_index": reverse("projects_index"),
        "projects_create": reverse("projects_create", args=["flow", "stage"]),
    }
