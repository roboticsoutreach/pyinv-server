from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.filtersets import NodeFilterSet
from assets.models import Node
from assets.serializers import NodeSerializer


class NodeViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetch information about nodes."""

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    filterset_class = NodeFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'created_at', 'updated_at', 'numchild', 'depth']

    @action(detail=True)
    def ancestors(self, request, pk=0):
        """Fetch the ancestors of a node."""
        node = self.get_object()
        ancestors = node.get_ancestors()
        return Response(NodeSerializer(ancestors, many=True).data)

    @action(detail=True)
    def children(self, request, pk=0):
        """Fetch the children of a node."""
        node = self.get_object()
        children = node.get_children()
        return Response(NodeSerializer(children, many=True).data)

    @action(detail=True)
    def descendents(self, request, pk=0):
        """Fetch the descendents of a node."""
        node = self.get_object()
        descendents = node.get_descendants()
        return Response(NodeSerializer(descendents, many=True).data)
