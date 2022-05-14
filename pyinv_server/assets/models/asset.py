import uuid

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    @property
    def display_name(self) -> str:
        if self.name is None or len(self.name) == 0:
            return str(self.asset_model)
        else:
            return self.name

    def __str__(self) -> str:
        return self.display_name  # TODO: Add Asset Code
