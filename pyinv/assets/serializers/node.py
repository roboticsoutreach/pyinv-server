from rest_framework import serializers

from assets.models import Node, NodeType

from .asset import AssetSerializer


class NodeLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to a node."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    node_type = serializers.ChoiceField(choices=NodeType.choices)
    is_container = serializers.BooleanField(read_only=True)
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = Node
        fields = ('id', 'node_type', 'display_name', 'is_container')


class NodeSerializer(serializers.ModelSerializer):
    """Serializer for nodes."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    name = serializers.CharField()
    node_type = serializers.ChoiceField(choices=NodeType.choices)
    asset = AssetSerializer()
    display_name = serializers.CharField(read_only=True)
    ancestors = serializers.ListField(child=NodeLinkSerializer(), read_only=True)
    is_container = serializers.BooleanField(read_only=True)

    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    numchild = serializers.IntegerField(read_only=True)
    depth = serializers.IntegerField(read_only=True)

    class Meta:
        model = Node
        fields = (
            'id',
            'name',
            'node_type',
            'asset',
            'display_name',
            'parent',
            'numchild',
            'depth',
            'ancestors',
            'is_container',
        )
