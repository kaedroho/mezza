from django.db import models

__all__ = [
    "Space",
]


class Space(models.Model):
    """
    A workspace that provides isolation for multiple tenants.
    """

    name = models.TextField(max_length=50)
    slug = models.TextField(max_length=50, unique=True)
