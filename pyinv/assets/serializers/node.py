from rest_framework import serializers

from assets.models import Node

from .asset import AssetSerializer
from .node_link import NodeLinkSerializer


class NodeSerializer(NodeLinkSerializer):
    """Serializer for nodes."""

    name = serializers.CharField()
    asset = AssetSerializer(read_only=True)

    ancestors = serializers.ListField(child=NodeLinkSerializer(), read_only=True)
    depth = serializers.IntegerField(read_only=True)

    class Meta:
        model = Node
        fields = NodeLinkSerializer.Meta.fields + (
            'name',
            'asset',
            'depth',
            'ancestors',
        )
