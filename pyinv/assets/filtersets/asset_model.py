import django_filters

from assets.models import AssetModel, Manufacturer


class AssetModelFilterSet(django_filters.FilterSet):

    manufacturer = django_filters.ModelChoiceFilter(
        field_name="manufacturer",
        to_field_name='slug',
        queryset=Manufacturer.objects.all(),
        label="Manufacturer",
    )
    is_container = django_filters.BooleanFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = AssetModel
        fields = [
            'is_container',
            'created_at',
            'updated_at',
        ]
