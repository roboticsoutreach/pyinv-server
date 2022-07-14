from typing import List

import django_filters
from django.contrib.auth.models import User

from assets.models import Asset, AssetEvent, ChangeSet


class AssetEventFilterSet(django_filters.FilterSet):

    asset = django_filters.ModelChoiceFilter(
        field_name="asset",
        to_field_name='id',
        queryset=Asset.objects.all(),
        label="Asset",
    )

    changeset = django_filters.ModelChoiceFilter(
        field_name="changeset",
        to_field_name='id',
        queryset=ChangeSet.objects.all(),
        label="ChangeSet",
    )

    user = django_filters.ModelChoiceFilter(
        field_name="changeset__user",
        to_field_name='username',
        queryset=User.objects.all(),
        label="User",
    )
    timestamp = django_filters.DateTimeFromToRangeFilter(field_name="changeset__timestamp")
    event_type = django_filters.MultipleChoiceFilter(choices=AssetEvent.AssetEventType.choices)

    class Meta:
        model = AssetEvent
        fields: List[str] = []
