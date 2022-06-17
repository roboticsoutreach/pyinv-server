from rest_framework import filters, viewsets

from assets.models import Manufacturer
from assets.serializers import ManufacturerSerializer


class ManufacturerViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetch information about manufacturers."""

    queryset = Manufacturer.objects.all()
    lookup_field = "slug"
    serializer_class = ManufacturerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name", "slug", 'created_at', 'updated_at']
    search_fields = ["name", "slug"]
