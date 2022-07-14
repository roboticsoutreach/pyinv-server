from django.db.models import Count, ProtectedError, query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from assets.filtersets import AssetModelFilterSet
from assets.models import AssetModel
from assets.serializers import AssetModelSerializer
from pyinv.api_exceptions import UnableToDelete


class AssetModelViewSet(viewsets.ModelViewSet):
    """Fetch information about asset models."""

    lookup_field = "slug"
    serializer_class = AssetModelSerializer
    filterset_class = AssetModelFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'asset_count', 'created_at', 'updated_at']
    search_fields = [
        'name',
        'slug',
        'manufacturer__name',
        'manufacturer__slug',
    ]

    def get_queryset(self) -> query.QuerySet[AssetModel]:
        return AssetModel.objects.annotate(asset_count=Count('asset')).all()

    def perform_destroy(self, instance: AssetModel) -> None:
        try:
            return super(AssetModelViewSet, self).perform_destroy(instance)
        except ProtectedError:
            raise UnableToDelete()
