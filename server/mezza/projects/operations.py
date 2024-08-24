from django.db.models import F

from mezza.models import Project


def create_project(*, title, description, space, stage):
    Project.objects.filter(space=space, stage=stage).update(order=F("order") + 1)

    return Project.objects.create(
        title=title, description=description, space=space, stage=stage, order=0
    )
