from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from assets.filtersets import NodeFilterSet
from assets.models import Node
from assets.serializers import NodeSerializer


class NodeViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Fetch information about nodes."""

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    filterset_class = NodeFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'created_at', 'updated_at', 'numchild', 'depth']
    search_fields = [
        'name',
        'asset__asset_model__name',
        'asset__asset_model__slug',
        'asset__asset_model__manufacturer__name',
        'asset__asset_model__manufacturer__slug',
        'asset__assetcode__code',
    ]
