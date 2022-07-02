from typing import Optional

import django_filters
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from assets.models import Node


class NodeFilterSet(django_filters.FilterSet):

    parent = django_filters.CharFilter(label="Parent", method='filter_parent')
    descendent_of = django_filters.CharFilter(label="Descendent of", method='filter_descendent_of')
    is_container = django_filters.BooleanFilter(method='filter_is_container', label="Is Container")

    def filter_parent(self, queryset: QuerySet[Node], name: str, value: str) -> QuerySet[Node]:
        if value == "root":
            return queryset & Node.get_root_nodes()
        try:
            parent = Node.objects.get(pk=value)
            return queryset & parent.get_children()
        except (Node.DoesNotExist, ValidationError):
            return Node.objects.none()

    def filter_descendent_of(self, queryset: QuerySet[Node], name: str, value: str) -> QuerySet[Node]:
        if value == "root":
            return queryset  # All nodes are a child of the root
        try:
            parent = Node.objects.get(pk=value)
            return queryset & parent.get_descendants()
        except (Node.DoesNotExist, ValidationError):
            return Node.objects.none()

    def filter_is_container(self, queryset: QuerySet[Node], name: str, value: Optional[bool]) -> QuerySet[Node]:
        if value is None:
            return queryset
        elif value is True:
            return (
                queryset.filter(node_type="A", asset__asset_model__is_container=True)
                | queryset.filter(node_type="L")
            )
        else:
            return queryset.filter(node_type="A", asset__asset_model__is_container=False)

    class Meta:
        model = Node
        fields = [
            'name',
            'parent',
            'node_type',
            'depth',
            'numchild',
        ]
