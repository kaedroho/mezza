from django.db import models

__all__ = [
    "Flow",
    "Stage",
]


class Stage(models.Model):
    title = models.TextField(max_length=200)
    order = models.IntegerField()
    space = models.ForeignKey(
        "crowflowspaces.Space", on_delete=models.CASCADE, related_name="stages"
    )
    is_custom = models.BooleanField(default=True)


class Flow(models.Model):
    title = models.TextField(max_length=200)
    space = models.ForeignKey(
        "crowflowspaces.Space", on_delete=models.CASCADE, related_name="flows"
    )
    stages = models.ManyToManyField("Stage", through="FlowStage", related_name="flows")
    initial_stage = models.ForeignKey(
        "Stage", on_delete=models.CASCADE, related_name="+"
    )


class FlowStage(models.Model):
    flow = models.ForeignKey("Flow", on_delete=models.CASCADE, related_name="+")
    stage = models.ForeignKey("Stage", on_delete=models.CASCADE, related_name="+")

    class Meta:
        unique_together = ("flow", "stage")
