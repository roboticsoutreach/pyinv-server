from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from assets.filtersets import AssetModelFilterSet
from assets.models import AssetModel
from assets.serializers import AssetModelSerializer


class AssetModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetch information about asset models."""

    queryset = AssetModel.objects.all()
    lookup_field = "slug"
    serializer_class = AssetModelSerializer
    filterset_class = AssetModelFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'created_at', 'updated_at']
    search_fields = [
        'name',
        'slug'
        'manufacturer__name',
        'manufacturer__slug',
    ]
