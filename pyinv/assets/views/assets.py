from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from assets.filtersets import AssetFilterSet
from assets.models import Asset
from assets.serializers import AssetSerializer


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetch information about assets."""

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filterset_class = AssetFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    search_fields = [
        'asset_model__name',
        'asset_model__slug',
        'asset_model__manufacturer__name',
        'asset_model__manufacturer__slug',
        'node__name',
        'assetcode__code',
    ]
