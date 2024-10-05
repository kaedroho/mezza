from django.db.models import F

from mezza.models import Project


def create_project(*, title, description, space):
    Project.objects.filter(space=space).update(order=F("order") + 1)

    return Project.objects.create(
        title=title, description=description, space=space, order=0
    )
