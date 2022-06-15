from assets.filtersets import AssetFilterSet
from assets.models import Asset
from assets.serializers import AssetSerializer
from rest_framework import viewsets


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetch information about assets."""

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    filterset_class = AssetFilterSet
