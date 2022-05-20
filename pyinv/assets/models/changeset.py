import uuid

from django.contrib.auth.models import User
from django.db import models


class Changeset(models.Model):
    """A group of changes that occurred at the same time."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Changeset: {self.timestamp} by {self.user}"
