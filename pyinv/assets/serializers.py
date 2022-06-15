from rest_framework import serializers

from .models import Asset, AssetState


class AssetSerializer(serializers.ModelSerializer):
    """
    Serializer for Asset objects.
    """

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    node = serializers.PrimaryKeyRelatedField(read_only=True)
    asset_model = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    asset_codes = serializers.ListField(child=serializers.CharField())
    state = serializers.ChoiceField(choices=AssetState.choices)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    extra_data = serializers.JSONField(default=dict, required=False)

    class Meta:
        model = Asset
        fields = (
            'id',
            'node',
            'asset_model',
            'asset_codes',
            'state',
            'created_at',
            'updated_at',
            'extra_data',
        )
