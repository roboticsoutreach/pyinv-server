from django.db.models import Count, query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, request, response, viewsets
from rest_framework.decorators import action

from assets.filtersets import ChangeSetFilterSet
from assets.models import ChangeSet
from assets.serializers import (
    AssetEventTimelineSerializer,
    ChangeSetSerializerWithCountSerializer,
)


class ChangeSetViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetch information about asset events."""

    # Require user to be logged in and have permissions, as this endpoint
    # returns some information about users.
    permission_classes = [permissions.DjangoModelPermissions]
    serializer_class = ChangeSetSerializerWithCountSerializer
    queryset = ChangeSet.objects.all()
    filterset_class = ChangeSetFilterSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['timestamp', 'event_count']
    search_fields = [
        'comment',
    ]

    def get_queryset(self) -> query.QuerySet[ChangeSet]:
        """Enable sorting by event_count."""
        return ChangeSet.objects.annotate(event_count=Count('assetevent')).all()

    @action(detail=True)
    def events(self, request: request.Request, pk: int = 0) -> response.Response:
        """Get the events in the changeset."""
        changeset = self.get_object()
        page = self.paginate_queryset(changeset.assetevent_set.all())
        serializer = AssetEventTimelineSerializer(instance=page, many=True)
        return self.get_paginated_response(serializer.data)
