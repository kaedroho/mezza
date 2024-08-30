from mezza.models import Space, SpaceUser


def create_space(*, name, slug, users=None):
    space = Space.objects.create(name=name, slug=slug)

    if users:
        for user in users:
            SpaceUser.objects.create(user=user, space=space)

    return space
