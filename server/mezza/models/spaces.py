from django.db import models

from .user import User

__all__ = [
    "Space",
    "SpaceUser",
]


class Space(models.Model):
    """
    A workspace that provides isolation for multiple tenants.
    """

    name = models.TextField(max_length=50)
    slug = models.TextField(max_length=50, unique=True)
    users = models.ManyToManyField(User, through="SpaceUser", related_name="spaces")


class SpaceUser(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="+")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        unique_together = [("space", "user")]
