from mezza.models import AssetLibrary, Space, SpaceUser


def create_space(*, name, slug, users=None):
    space = Space.objects.create(name=name, slug=slug)

    if users:
        for user in users:
            SpaceUser.objects.create(user=user, space=space)

    # Create default asset library
    AssetLibrary.objects.create(space=space, name="Default")

    return space
