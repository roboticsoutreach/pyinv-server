import uuid
from typing import List, Optional

from django.db import models

from .asset_model import AssetModel


class Asset(models.Model):
    """An individual, tracked asset."""

    class State(models.TextChoices):
        KNOWN = 'K', 'Known'  # A known asset that we currently own.
        LOST = 'L', 'Lost'  # A known asset that we currently own.
        DISPOSED = 'D', 'Disposed'  # An asset that has been disposed of.

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    name = models.CharField(max_length=30, null=True, blank=True)
    asset_model = models.ForeignKey(AssetModel, on_delete=models.PROTECT)
    state = models.CharField(
        max_length=1,
        choices=State.choices,
        default=State.KNOWN,
    )

    location = models.ForeignKey(
        'assets.Location',
        on_delete=models.PROTECT,
        related_name="contents",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:

        constraints = [
            models.CheckConstraint(
                check=models.Q(state="K", location__isnull=False) |
                models.Q(state="L", location__isnull=True) |
                models.Q(state="D", location__isnull=True),
                name='valid_state',
            ),
        ]

    @property
    def display_name(self) -> str:
        if self.name is None or len(self.name) == 0:
            return str(self.asset_model)
        else:
            return self.name

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
        return [code.code for code in self.assetcode_set.all()]

    def __str__(self) -> str:
        return f"{self.display_name} ({self.first_asset_code})"

    @classmethod
    def get_by_code(cls, code: str) -> Optional['Asset']:
        """Get an asset by its asset code."""
        return cls.objects.filter(assetcode__code=code).first()
