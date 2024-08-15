from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from crowflow.spaces.models import Space

__all__ = [
    "Stage",
    "Flow",
]


class Stage(models.Model):
    title = models.TextField(max_length=200)
    order = models.IntegerField()
    space = models.ForeignKey(
        "crowflowspaces.Space", on_delete=models.CASCADE, related_name="stages"
    )


class Flow(models.Model):
    title = models.TextField(max_length=200)
    space = models.ForeignKey(
        "crowflowspaces.Space", on_delete=models.CASCADE, related_name="flows"
    )
    stages = models.ManyToManyField("Stage", related_name="flows")


@receiver(post_save, sender=Space)
def create_default_flows(sender, instance, created, **kwargs):
    if created:
        idea_stage = Stage.objects.create(title="Idea", order=1, space=instance)
        todo_stage = Stage.objects.create(title="Todo", order=2, space=instance)
        scripting_stage = Stage.objects.create(
            title="Scripting", order=3, space=instance
        )
        filming_stage = Stage.objects.create(title="Filming", order=4, space=instance)
        editing_stage = Stage.objects.create(title="Editing", order=5, space=instance)
        ready_to_publish_stage = Stage.objects.create(
            title="Ready to publish", order=6, space=instance
        )
        scheduled_stage = Stage.objects.create(
            title="Scheduled", order=7, space=instance
        )
        published_stage = Stage.objects.create(
            title="Published", order=8, space=instance
        )

        videos_flow = Flow.objects.create(
            title="Videos",
            space=instance,
        )

        videos_flow.stages.set(
            [
                idea_stage,
                todo_stage,
                scripting_stage,
                filming_stage,
                editing_stage,
                ready_to_publish_stage,
                scheduled_stage,
                published_stage,
            ]
        )
