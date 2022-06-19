from django.db.models import ProtectedError
from rest_framework import filters, viewsets

from assets.models import Manufacturer
from assets.serializers import ManufacturerSerializer
from pyinv.api_exceptions import UnableToDelete

class ManufacturerViewSet(viewsets.ModelViewSet):
    """Fetch information about manufacturers."""

    queryset = Manufacturer.objects.all()
    lookup_field = "slug"
    serializer_class = ManufacturerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name", "slug", 'created_at', 'updated_at']
    search_fields = ["name", "slug"]

    def perform_destroy(self, instance):
        try:
            return super(ManufacturerViewSet, self).perform_destroy(instance)
        except ProtectedError:
            raise UnableToDelete()
