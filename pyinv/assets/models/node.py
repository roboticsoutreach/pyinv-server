"""Asset Tree Node."""

from typing import Optional
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from treebeard.mp_tree import MP_Node


class NodeType(models.TextChoices):
    """The type of node."""

    ASSET = 'A', 'Asset'
    LOCATION = 'L', 'Location'


class Node(MP_Node):
    """A node in the asset tree."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # noqa: A003
    name = models.CharField(max_length=100, blank=True, null=True)
    node_type = models.CharField(max_length=1, choices=NodeType.choices)
    asset = models.OneToOneField('Asset', on_delete=models.PROTECT, blank=True, null=True)

    def clean(self) -> None:
        """Validate the node."""
        if self.node_type == NodeType.ASSET:
            if self.asset is None:
                raise ValidationError('Asset nodes must have an associated asset.')
        elif self.node_type == NodeType.LOCATION:
            if self.asset is not None:
                raise ValidationError('Location nodes cannot have an associated asset.')

            if self.name is None:
                raise ValidationError('Location nodes must have a name.')

    class Meta:

        constraints = [
            models.CheckConstraint(
                check=models.Q(node_type=NodeType.ASSET, asset__isnull=False) |
                models.Q(node_type=NodeType.LOCATION, asset__isnull=True),
                name='node_type_asset_null_check',
            ),
            models.CheckConstraint(
                check=models.Q(node_type=NodeType.LOCATION, name__isnull=False) |
                models.Q(node_type=NodeType.ASSET),
                name='node_type_force_name_if_asset',
            )
        ]

    @property
    def parent(self) -> Optional['Node']:
        return self.get_parent()

    @property
    def ancestors(self):
        return self.get_ancestors().all()

    @property
    def is_container(self) -> bool:
        return self.node_type == NodeType.LOCATION or self.asset.asset_model.is_container

    @property
    def display_name(self) -> str:
        if self.node_type == NodeType.ASSET:
            return self.asset.display_name
        else:
            return self.name

    def __str__(self):
        return self.display_name

    def mark_out_of_tree(self, recursive: bool) -> None:
        """Mark the node and all of its descendants as out of tree."""
        if not recursive and self.get_descendants().count() > 0:
            raise ValueError('Cannot mark a non-empty node as lost.')

        self.delete()
