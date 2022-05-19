import uuid

from django.db import models

from .asset import Asset

ASSET_EVENT_TYPES = [
    ('A', 'Added'),
    ('M', 'Moved'),
    ('U', 'Updated'),
]


class AssetEvent(models.Model):
    """An event that has occurred to an asset.."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    changeset = models.ForeignKey('Changeset', on_delete=models.PROTECT)
    event_type = models.CharField(max_length=1, choices=ASSET_EVENT_TYPES)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    data = models.JSONField()

    def __str__(self) -> str:
        return f"Event: {self.event_type} on {self.asset}"
