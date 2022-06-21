from rest_framework import serializers

from assets.models import Node, NodeType


class NodeLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to a node."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    display_name = serializers.CharField(read_only=True)
    node_type = serializers.ChoiceField(choices=NodeType.choices)
    is_container = serializers.BooleanField(read_only=True)
    numchild = serializers.IntegerField(read_only=True)

    class Meta:
        model = Node
        fields = ('id', 'display_name', 'node_type', 'numchild', 'is_container')


class NodeLinkWithParentSerializer(NodeLinkSerializer):

    parent = NodeLinkSerializer(read_only=True)

    class Meta:
        model = Node
        fields = NodeLinkSerializer.Meta.fields + (
            'parent',
        )
