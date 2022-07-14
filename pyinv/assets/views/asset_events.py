from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from assets.filtersets import AssetEventFilterSet
from assets.models import AssetEvent
from assets.serializers import AssetEventWithAssetSerializer


class AssetEventViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetch information about asset events."""

    # Require user to be logged in and have permissions, as this endpoint
    # returns some information about users.
    permission_classes = [permissions.DjangoModelPermissions]

    queryset = AssetEvent.objects.all()
    serializer_class = AssetEventWithAssetSerializer
    filterset_class = AssetEventFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['changeset__timestamp']
    search_fields = [
        'changeset__comment',
    ]
