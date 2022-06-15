"""Asset Information."""

from typing import List
from uuid import uuid4

from django.db import models

from .asset_model import AssetModel


class AssetState(models.TextChoices):
    KNOWN = 'K', 'Known'  # A known asset that we currently own.
    LOST = 'L', 'Lost'  # A known asset that we currently own.
    DISPOSED = 'D', 'Disposed'  # An asset that has been disposed of.


class Asset(models.Model):
    """Asset."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # noqa: A003
    state = models.CharField(
        max_length=1,
        choices=AssetState.choices,
        default=AssetState.KNOWN,
    )
    asset_model = models.ForeignKey(AssetModel, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    @property
    def display_name(self) -> str:
        try:
            return self.node.name or str(self.asset_model)
        except Asset.node.RelatedObjectDoesNotExist:
            return str(self.asset_model)

    @property
    def first_asset_code(self) -> str:
        """A usable asset code for the asset."""
        code = self.assetcode_set.first()
        if code is None:
            return str(self.id)
        else:
            return code.code

    @property
    def asset_codes(self) -> List[str]:
        """A list of all asset codes for the asset."""
        return [str(self.id)] + [code.code for code in self.assetcode_set.all()]

    def __str__(self) -> str:
        return f"{self.display_name} ({self.first_asset_code})"
