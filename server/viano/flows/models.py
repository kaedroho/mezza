from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from viano.spaces.models import Space

__all__ = [
    "Stage",
    "Flow",
]


class Stage(models.Model):
    title = models.TextField(max_length=200)
    order = models.IntegerField()
    space = models.ForeignKey(
        "vianospaces.Space", on_delete=models.CASCADE, related_name="stages"
    )

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["space", "order"]


class Flow(models.Model):
    title = models.TextField(max_length=200)
    space = models.ForeignKey(
        "vianospaces.Space", on_delete=models.CASCADE, related_name="flows"
    )
    stages = models.ManyToManyField("Stage", related_name="flows")

    def __str__(self):
        return self.title


@receiver(post_save, sender=Space)
def create_default_flows(sender, instance, created, **kwargs):
    if created:
        idea_stage = Stage.objects.create(title="Idea", order=1, space=instance)
        scripting_stage = Stage.objects.create(
            title="Scripting", order=3, space=instance
        )
        filming_stage = Stage.objects.create(title="Filming", order=4, space=instance)
        editing_stage = Stage.objects.create(title="Editing", order=5, space=instance)
        completed_stage = Stage.objects.create(
            title="Completed", order=6, space=instance
        )

        videos_flow = Flow.objects.create(
            title="Video",
            space=instance,
        )

        videos_flow.stages.set(
            [
                idea_stage,
                scripting_stage,
                filming_stage,
                editing_stage,
                completed_stage,
            ]
        )
