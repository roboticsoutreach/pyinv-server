from typing import List

import django_filters
from django.contrib.auth.models import User

from assets.models import ChangeSet


class ChangeSetFilterSet(django_filters.FilterSet):

    user = django_filters.ModelChoiceFilter(
        to_field_name='username',
        queryset=User.objects.all(),
        label="User",
    )
    timestamp = django_filters.DateTimeFromToRangeFilter()
    event_count = django_filters.RangeFilter(label="Number of Events")

    class Meta:
        model = ChangeSet
        fields: List[str] = []
