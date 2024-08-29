from django.contrib import messages
from django.db.models import F
from django.urls import reverse
from django_bridge.response import CloseOverlayResponse, Response

from mezza.models import Idea

from .forms import IdeaForm
from .operations import create_project_from_idea


def ideas_index(request):
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    return Response(
        request,
        "IdeasIndex",
        {
            "ideas": [idea.to_client_representation() for idea in space.ideas.all()],
        },
    )


def ideas_create(request):
    # FIXME: Get space from URL
    space = request.user.spaces.first()
    form = IdeaForm(request.POST or None)

    if form.is_valid():
        idea = form.save(commit=False)
        idea.space = space

        # Order the idea at the start
        idea.order = 0
        space.ideas.update(order=F("order") + 1)

        idea.save()

        messages.success(
            request,
            f"Successfully created idea '{idea.title}'.",
        )

        return CloseOverlayResponse(request)

    return Response(
        request,
        "ProjectsForm",
        {
            "title": "New Idea",
            "action_url": reverse("ideas_create"),
            "form": form,
        },
        overlay=True,
        title="New Idea | Mezza Studio",
    )


def ideas_start_production(request, idea_id):
    idea = Idea.objects.get(id=idea_id)

    if request.method == "POST":
        create_project_from_idea(idea)
        idea.delete()

        messages.success(
            request,
            f"Successfully started production on idea '{idea.title}'.",
        )

        return CloseOverlayResponse(request)

    return Response(
        request,
        "IdeasStartProduction",
        {
            "action_url": reverse("ideas_start_production", args=[idea_id]),
        },
        overlay=True,
        title="Start Production | Mezza Studio",
    )
