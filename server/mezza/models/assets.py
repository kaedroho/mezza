from django.db import models
from polymorphic.models import PolymorphicModel

from .projects import Project
from .spaces import Space

__all__ = [
    "AssetLibrary",
    "Asset",
]


class AssetLibrary(models.Model):
    space = models.ForeignKey(
        Space, on_delete=models.CASCADE, related_name="asset_libraries"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Asset(PolymorphicModel):
    # An asset can belong to either an asset library or a project, but not both.
    library = models.ForeignKey(
        AssetLibrary, on_delete=models.CASCADE, null=True, related_name="assets"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name="assets"
    )
    name = models.CharField(max_length=255)

    def to_client_representation(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.polymorphic_ctype.model,
        }

    def __str__(self):
        return self.name
