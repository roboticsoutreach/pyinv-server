from typing import Any, Dict

from rest_framework import serializers

from assets.models import AssetModel, Manufacturer, Node
from pyinv.api_exceptions import UnableToChangeContainerState

from .manufacturer import ManufacturerLinkSerializer


class AssetModelLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to an asset model."""

    class Meta:
        model = AssetModel
        fields = ('name', 'slug')


class AssetModelSerializer(serializers.ModelSerializer):
    """Serializer for AssetModel objects."""
    slug = serializers.CharField(allow_null=True, required=False)
    manufacturer = ManufacturerLinkSerializer(read_only=True)
    manufacturer_slug = serializers.SlugRelatedField(
        slug_field="slug",
        source="manufacturer",
        queryset=Manufacturer.objects.all()
    )
    is_container = serializers.BooleanField(default=False)
    asset_count = serializers.IntegerField(read_only=True, source="asset_set.count")

    class Meta:
        model = AssetModel
        fields = (
            'name',
            'slug',
            'manufacturer',
            'manufacturer_slug',
            'is_container',
            'asset_count',
            'created_at',
            'updated_at',
        )

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # If we are updating an existing model to not be a container, check that all of the associated
        # nodes are empty.
        if self.instance and "is_container" in data and not data["is_container"]:
            assets = self.instance.asset_set.all()  # type: ignore[union-attr]
            if Node.objects.filter(asset__in=assets, numchild__gt=0).exists():
                raise UnableToChangeContainerState()
        return data
