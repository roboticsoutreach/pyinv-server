import django_filters
from django.core.exceptions import ValidationError

from .models import Asset, AssetModel


class AssetFilterSet(django_filters.FilterSet):

    asset_code = django_filters.CharFilter(label="Asset Code", method='filter_asset_code')
    has_node = django_filters.BooleanFilter(
        field_name='node',
        lookup_expr='isnull',
        exclude=True,
        label="Has Node",
    )
    asset_model = django_filters.ModelChoiceFilter(
        field_name="asset_model",
        to_field_name='slug',
        queryset=AssetModel.objects.all(),
        label="Asset Model",
    )
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    def filter_asset_code(self, queryset, name, value):
        qs = queryset.filter(assetcode__code=value)
        try:
            qs = qs | queryset.filter(id=value)
        except ValidationError:
            pass
        return qs

    class Meta:
        model = Asset
        fields = [
            'asset_model',
            'state',
            'created_at',
            'updated_at',
            'has_node',
        ]
