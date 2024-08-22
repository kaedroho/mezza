from mezza.models import Pipeline, Space, SpaceUser, Stage


def create_space(*, name, slug, users=None):
    space = Space.objects.create(name=name, slug=slug)

    if users:
        for user in users:
            SpaceUser.objects.create(user=user, space=space)

    # Create default pipeline
    idea_stage = Stage.objects.create(title="Ideas", order=1, space=space)
    scripting_stage = Stage.objects.create(title="Scripting", order=3, space=space)
    filming_stage = Stage.objects.create(title="Filming", order=4, space=space)
    editing_stage = Stage.objects.create(title="Editing", order=5, space=space)
    completed_stage = Stage.objects.create(title="Completed", order=6, space=space)

    videos_Pipeline = Pipeline.objects.create(
        title="Video",
        space=space,
    )

    videos_Pipeline.stages.set(
        [
            idea_stage,
            scripting_stage,
            filming_stage,
            editing_stage,
            completed_stage,
        ]
    )
