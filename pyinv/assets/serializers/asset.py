from rest_framework import serializers

from assets.models import Asset, Node

from .asset_model import AssetModelLinkSerializer


class AssetNodeParentLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to a node's parent."""

    class Meta:
        model = Node
        fields = ('id', 'display_name')


class AssetNodeLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to a node."""

    parent = AssetNodeParentLinkSerializer(read_only=True)

    class Meta:
        model = Node
        fields = ('id', 'display_name', 'numchild', 'parent')


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset objects."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    node = AssetNodeLinkSerializer(read_only=True)
    asset_model = AssetModelLinkSerializer(read_only=True)
    asset_codes = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    extra_data = serializers.JSONField(default=dict, required=False)

    class Meta:
        model = Asset
        fields = (
            'id',
            'node',
            'asset_model',
            'asset_codes',
            'first_asset_code',
            'state',
            'created_at',
            'updated_at',
            'extra_data',
        )
