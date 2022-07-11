import uuid

from django.contrib.auth.models import User
from django.db import models

from assets.models.asset import Asset


class ChangeSet(models.Model):
    """
    A group of changes that occurred simultaneously.

    A typical changeset with multiple events would be doing an action to a
    group of assets at the same time.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.timestamp} by {self.user}"


class AssetEvent(models.Model):
    """A recorded change that happened to an asset."""

    class AssetEventType(models.TextChoices):

        CREATE = 'CR', "Create"
        MOVE = 'MV', "Move"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    event_type = models.CharField(max_length=2, choices=AssetEventType.choices)
    changeset = models.ForeignKey(ChangeSet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    data = models.JSONField()

    class Meta:
        unique_together = ('changeset', 'asset',)  # Asset can only appear once in changeset

    def __str__(self) -> str:
        return f"{self.event_type} on {self.asset} at {self.changeset.timestamp}"
