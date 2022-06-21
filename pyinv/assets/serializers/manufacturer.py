from rest_framework import serializers

from assets.models import Manufacturer


class ManufacturerLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to a manufacturer."""

    class Meta:
        model = Manufacturer
        fields = ('name', 'slug')


class ManufacturerSerializer(serializers.ModelSerializer):
    """Serializer for Manufacturer."""
    slug = serializers.CharField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Manufacturer
        fields = ('name', 'slug', 'created_at', 'updated_at')
