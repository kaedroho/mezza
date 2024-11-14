from mezza.models import Space, SpaceUser


def create_space(*, name, slug, users=None):
    space = Space.objects.create(name=name, slug=slug)

    if users:
        SpaceUser.objects.bulk_create(
            [SpaceUser(user=user, space=space) for user in users]
        )

    return space
