from rest_framework import serializers

from assets.models import Asset

from .asset_model import AssetModelLinkSerializer
from .node_link import NodeLinkWithParentSerializer


class AssetLinkSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)  # noqa: A003

    class Meta:
        model = Asset
        fields = (
            'id',
            'display_name',
        )


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset objects."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    asset_model = AssetModelLinkSerializer(read_only=True)
    asset_codes = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    extra_data = serializers.JSONField(default=dict, required=False)

    class Meta:
        model = Asset
        fields = (
            'id',
            'display_name',
            'asset_model',
            'asset_codes',
            'first_asset_code',
            'created_at',
            'updated_at',
            'extra_data',
        )


class AssetWithNodeSerializer(AssetSerializer):
    """Serializer for Asset objects."""

    node = NodeLinkWithParentSerializer(read_only=True)

    class Meta:
        model = Asset
        fields = AssetSerializer.Meta.fields + (
            'node',
        )
