from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .spaces import Space

__all__ = [
    "Stage",
    "Pipeline",
]


class Stage(models.Model):
    title = models.TextField(max_length=200)
    order = models.IntegerField()
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="stages")

    def to_client_representation(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["space", "order"]


class Pipeline(models.Model):
    title = models.TextField(max_length=200)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="Pipelines")
    stages = models.ManyToManyField("Stage", related_name="Pipelines")

    def __str__(self):
        return self.title


@receiver(post_save, sender=Space)
def create_default_Pipelines(sender, instance, created, **kwargs):
    if created:
        idea_stage = Stage.objects.create(title="Ideas", order=1, space=instance)
        scripting_stage = Stage.objects.create(
            title="Scripting", order=3, space=instance
        )
        filming_stage = Stage.objects.create(title="Filming", order=4, space=instance)
        editing_stage = Stage.objects.create(title="Editing", order=5, space=instance)
        completed_stage = Stage.objects.create(
            title="Completed", order=6, space=instance
        )

        videos_Pipeline = Pipeline.objects.create(
            title="Video",
            space=instance,
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
