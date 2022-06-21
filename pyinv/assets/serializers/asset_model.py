from rest_framework import serializers

from assets.models import AssetModel, Manufacturer

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
