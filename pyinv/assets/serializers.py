from rest_framework import serializers

from .models import Asset, AssetModel, Manufacturer, Node, NodeType


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset objects."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    node = serializers.PrimaryKeyRelatedField(read_only=True)
    asset_model = serializers.SlugRelatedField(slug_field="slug", read_only=True)
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
            'state',
            'created_at',
            'updated_at',
            'extra_data',
        )


class AssetModelSerializer(serializers.ModelSerializer):
    """Serializer for AssetModel objects."""
    manufacturer = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = AssetModel
        fields = ('name', 'slug', 'manufacturer', 'is_container', 'created_at', 'updated_at', )


class ManufacturerSerializer(serializers.ModelSerializer):
    """Serializer for Manufacturer."""
    asset_models = serializers.SlugRelatedField(source="assetmodel_set", slug_field="slug", read_only=True, many=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Manufacturer
        fields = ('name', 'slug', 'created_at', 'updated_at', 'asset_models')


class NodeSerializer(serializers.ModelSerializer):
    """Serializer for nodes."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    name = serializers.CharField()
    node_type = serializers.ChoiceField(choices=NodeType.choices)
    asset = serializers.PrimaryKeyRelatedField(read_only=True)
    display_name = serializers.CharField(read_only=True)

    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    numchild = serializers.IntegerField(read_only=True)
    depth = serializers.IntegerField(read_only=True)

    class Meta:
        model = Node
        fields = (
            'id', 'name', 'node_type', 'asset', 'display_name', 'parent', 'numchild', 'depth',
        )
